import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Updated imports for latest LangGraph
from langgraph.graph import StateGraph, END, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from typing import Sequence, Annotated, TypedDict, Optional, Dict, Any, List
import operator
import re
import json
from datetime import datetime

# Initialize Gemma 2B
llm = ChatOllama(
    model="gemma:2b",
    temperature=0.3,
)

# Define State Schema with proper typing
class DocState(TypedDict):
    messages: Annotated[List[BaseMessage], operator.add]
    needs_summary: bool
    original_text: str
    analysis_results: Dict[str, Any]
    processing_step: str

# ----------------------
# Node Implementations
# ----------------------
def extract_keywords(state: DocState) -> Dict[str, Any]:
    """Extract keywords from the original text"""
    original_text = state.get("original_text", "")
    if not original_text:
        return {
            "messages": [SystemMessage(content="No text to analyze")],
            "analysis_results": {"keywords": []},
            "processing_step": "keywords_failed"
        }
    
    prompt = ChatPromptTemplate.from_template(
        """Extract exactly 3 main keywords from this text. Respond with ONLY the keywords separated by commas. Do not include any other text, explanations, or phrases.

        Examples:
        Text: "The car was fast and red" -> fast, car, red
        Text: "I love programming in Python" -> programming, Python, love
        
        Text: {text}
        
        Keywords:"""
    )
    
    try:
        chain = prompt | llm
        response = chain.invoke({"text": original_text})
        keywords_raw = response.content.strip()
        
        # More aggressive cleaning to remove conversational text
        # Remove common conversational starters
        keywords_raw = re.sub(r'^(Sure,?\s*here are the|Here are the|The keywords are|Keywords?:?)\s*', '', keywords_raw, flags=re.IGNORECASE)
        keywords_raw = re.sub(r'\s*main keywords.*?:', '', keywords_raw, flags=re.IGNORECASE)
        
        # Split by commas and clean each keyword
        keywords = []
        for keyword in keywords_raw.split(','):
            # Clean each keyword
            clean_keyword = re.sub(r'[^\w\s]', '', keyword.strip())
            clean_keyword = ' '.join(clean_keyword.split())  # Normalize whitespace
            if clean_keyword and len(clean_keyword) > 1:
                keywords.append(clean_keyword)
        
        # Take only the first 3 valid keywords
        keywords = keywords[:3]
        
        # If we still don't have good keywords, fall back to simple extraction
        if not keywords or len(keywords) < 2:
            words = re.findall(r'\b[a-zA-Z]{3,}\b', original_text)
            keywords = list(dict.fromkeys(words))[:3]  # Remove duplicates, keep order
        
        return {
            "messages": [SystemMessage(content=f"Keywords extracted: {', '.join(keywords)}")],
            "analysis_results": {"keywords": keywords},
            "processing_step": "keywords_complete"
        }
    except Exception as e:
        return {
            "messages": [SystemMessage(content=f"Error extracting keywords: {str(e)}")],
            "analysis_results": {"keywords": [], "error": str(e)},
            "processing_step": "keywords_failed"
        }

def analyze_sentiment(state: DocState) -> Dict[str, Any]:
    """Analyze sentiment of the original text"""
    original_text = state.get("original_text", "")
    if not original_text:
        return {
            "messages": [SystemMessage(content="No text to analyze")],
            "analysis_results": {**state.get("analysis_results", {}), "sentiment": "unknown"},
            "processing_step": "sentiment_failed"
        }
    
    prompt = ChatPromptTemplate.from_template(
        """Analyze the sentiment of this text. Respond with only one word: positive, neutral, or negative.
        
        Text: {text}
        
        Sentiment:"""
    )
    
    try:
        chain = prompt | llm
        response = chain.invoke({"text": original_text})
        sentiment_raw = response.content.strip().lower()
        
        # Extract sentiment with better parsing
        if any(word in sentiment_raw for word in ["positive", "good", "excellent", "great"]):
            sentiment = "positive"
        elif any(word in sentiment_raw for word in ["negative", "bad", "terrible", "awful"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate confidence based on text features
        confidence = calculate_sentiment_confidence(original_text, sentiment)
        
        current_results = state.get("analysis_results", {})
        current_results.update({
            "sentiment": sentiment,
            "sentiment_confidence": confidence
        })
        
        return {
            "messages": [SystemMessage(content=f"Sentiment: {sentiment} (confidence: {confidence:.2f})")],
            "analysis_results": current_results,
            "processing_step": "sentiment_complete"
        }
    except Exception as e:
        current_results = state.get("analysis_results", {})
        current_results.update({"sentiment": "unknown", "error": str(e)})
        return {
            "messages": [SystemMessage(content=f"Error analyzing sentiment: {str(e)}")],
            "analysis_results": current_results,
            "processing_step": "sentiment_failed"
        }

def calculate_sentiment_confidence(text: str, sentiment: str) -> float:
    """Calculate confidence score for sentiment analysis"""
    positive_words = ["excellent", "great", "amazing", "wonderful", "fantastic", "love", "perfect"]
    negative_words = ["terrible", "awful", "hate", "horrible", "worst", "bad", "disappointing"]
    
    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)
    
    if sentiment == "positive" and pos_count > 0:
        return min(0.8 + (pos_count * 0.1), 1.0)
    elif sentiment == "negative" and neg_count > 0:
        return min(0.8 + (neg_count * 0.1), 1.0)
    elif sentiment == "neutral":
        return 0.6 + (0.2 if pos_count == neg_count else 0)
    else:
        return 0.5

def summarize(state: DocState) -> Dict[str, Any]:
    """Summarize the original text"""
    original_text = state.get("original_text", "")
    if not original_text:
        return {
            "messages": [SystemMessage(content="No text to summarize")],
            "analysis_results": {**state.get("analysis_results", {}), "summary": ""},
            "processing_step": "summary_failed"
        }
    
    if len(original_text) < 20:
        current_results = state.get("analysis_results", {})
        current_results.update({"summary": original_text})
        return {
            "messages": [SystemMessage(content="Text too short - using original as summary")],
            "analysis_results": current_results,
            "processing_step": "summary_complete"
        }
    
    prompt = ChatPromptTemplate.from_template(
        """Summarize this text in exactly one clear sentence. Keep it under 20 words. Respond with ONLY the summary sentence, no extra text.

        Examples:
        Text: "The car was very fast and painted bright red" -> "The car was fast and red"
        Text: "I really love programming in Python because it's easy" -> "User enjoys Python programming for its simplicity"
        
        Text: {text}
        
        Summary:"""
    )
    
    try:
        chain = prompt | llm
        response = chain.invoke({"text": original_text})
        summary_raw = response.content.strip()
        
        # More aggressive cleaning for summary
        summary = re.sub(r'^(Sure,?\s*here\'s|Here\'s|Summary:?|This is)\s*', '', summary_raw, flags=re.IGNORECASE)
        summary = re.sub(r'a summary.*?:', '', summary, flags=re.IGNORECASE)
        summary = summary.strip().rstrip(':').strip()
        
        # Ensure it's a proper sentence
        if summary and not summary.endswith('.'):
            summary += '.'
        
        # Limit length
        summary = summary[:150]
        
        # Calculate summary quality score
        quality_score = calculate_summary_quality(original_text, summary)
        
        current_results = state.get("analysis_results", {})
        current_results.update({
            "summary": summary,
            "summary_quality": quality_score
        })
        
        return {
            "messages": [SystemMessage(content=f"Summary: {summary}")],
            "analysis_results": current_results,
            "processing_step": "summary_complete"
        }
    except Exception as e:
        current_results = state.get("analysis_results", {})
        current_results.update({"summary": "", "error": str(e)})
        return {
            "messages": [SystemMessage(content=f"Error summarizing: {str(e)}")],
            "analysis_results": current_results,
            "processing_step": "summary_failed"
        }

def calculate_summary_quality(original: str, summary: str) -> float:
    """Calculate quality score for summary"""
    if not summary or len(summary) < 5:
        return 0.0
    
    # Check if summary is too similar to original (might indicate poor summarization)
    similarity = len(set(original.lower().split()) & set(summary.lower().split())) / len(set(original.lower().split()))
    
    # Ideal summary should capture key information but be significantly shorter
    length_ratio = len(summary) / len(original)
    ideal_ratio = 0.3  # 30% of original length is often good
    
    length_score = 1.0 - abs(length_ratio - ideal_ratio)
    content_score = min(similarity * 2, 1.0)  # Want some overlap but not too much
    
    return (length_score + content_score) / 2

def human_review(state: DocState) -> Dict[str, Any]:
    """Handle human review for sensitive content"""
    original_text = state.get("original_text", "")
    if not original_text:
        return {
            "messages": [SystemMessage(content="Nothing to review")],
            "analysis_results": {**state.get("analysis_results", {}), "review_status": "no_content"},
            "processing_step": "review_failed"
        }
    
    print(f"\n{'='*60}")
    print("🔍 HUMAN REVIEW REQUIRED")
    print(f"Text: {original_text}")
    print(f"Length: {len(original_text)} characters")
    print(f"Detected sensitive keywords")
    print('='*60)
    
    try:
        while True:
            approval = input("Approve this content? (y/n/s for skip): ").lower().strip()
            if approval in ['y', 'yes']:
                status = "approved"
                break
            elif approval in ['n', 'no']:
                status = "rejected"
                break
            elif approval in ['s', 'skip']:
                status = "skipped"
                break
            else:
                print("Please enter 'y' for yes, 'n' for no, or 's' to skip")
        
        current_results = state.get("analysis_results", {})
        current_results.update({
            "review_status": status,
            "review_timestamp": datetime.now().isoformat()
        })
        
        return {
            "messages": [SystemMessage(content=f"Review completed: {status}")],
            "analysis_results": current_results,
            "processing_step": "review_complete"
        }
    except KeyboardInterrupt:
        current_results = state.get("analysis_results", {})
        current_results.update({"review_status": "cancelled"})
        return {
            "messages": [SystemMessage(content="Review cancelled by user")],
            "analysis_results": current_results,
            "processing_step": "review_cancelled"
        }

# ----------------------
# Enhanced Routing Logic
# ----------------------
def route_after_summary(state: DocState) -> str:
    """Route based on content sensitivity with enhanced detection"""
    original_text = state.get("original_text", "").lower()
    
    # Enhanced sensitive keywords detection
    sensitive_keywords = {
        "confidential", "sensitive", "private", "secret", "classified",
        "proprietary", "internal", "restricted", "personal", "medical",
        "financial", "ssn", "credit card", "password", "login"
    }
    
    # Check for patterns that might indicate sensitive content
    sensitive_patterns = [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
        r'\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b',  # Credit card pattern
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Email pattern
    ]
    
    # Check keywords
    has_sensitive_keywords = any(keyword in original_text for keyword in sensitive_keywords)
    
    # Check patterns
    has_sensitive_patterns = any(re.search(pattern, original_text) for pattern in sensitive_patterns)
    
    needs_review = has_sensitive_keywords or has_sensitive_patterns
    
    return "review" if needs_review else "sentiment"

def should_end_workflow(state: DocState) -> str:
    """Determine if workflow should end based on review status"""
    analysis_results = state.get("analysis_results", {})
    review_status = analysis_results.get("review_status", "")
    
    if review_status == "rejected":
        return END
    elif review_status in ["approved", "skipped"]:
        return "sentiment"
    else:
        return "sentiment"

# ----------------------
# Graph Construction
# ----------------------
def create_workflow():
    """Create and configure the workflow graph"""
    workflow = StateGraph(DocState)
    
    # Add nodes
    workflow.add_node("keywords", extract_keywords)
    workflow.add_node("sentiment", analyze_sentiment)
    workflow.add_node("summary", summarize)
    workflow.add_node("review", human_review)
    
    # Set entry point
    workflow.set_entry_point("keywords")
    
    # Add edges
    workflow.add_edge("keywords", "summary")
    workflow.add_edge("sentiment", END)
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "summary",
        route_after_summary,
        {"review": "review", "sentiment": "sentiment"}
    )
    
    workflow.add_conditional_edges(
        "review",
        should_end_workflow,
        {"sentiment": "sentiment", END: END}
    )
    
    return workflow

# ----------------------
# Enhanced Execution Setup
# ----------------------
def process_document(text: str, thread_id: str = "default", save_results: bool = False) -> Dict[str, Any]:
    """Process a document through the analysis pipeline"""
    
    if not text or not text.strip():
        print("Error: Empty text provided")
        return {}
    
    # Create workflow and compile with memory
    workflow = create_workflow()
    checkpointer = MemorySaver()
    app = workflow.compile(checkpointer=checkpointer)
    
    # Configure thread
    config = {"configurable": {"thread_id": thread_id}}
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=text)],
        "needs_summary": True,
        "original_text": text,
        "analysis_results": {},
        "processing_step": "initialized"
    }
    
    print(f"\n📄 Processing Document (ID: {thread_id})")
    print(f"Text: '{text[:80]}{'...' if len(text) > 80 else ''}'")
    print(f"Length: {len(text)} characters")
    
    try:
        # Run the workflow
        result = app.invoke(initial_state, config=config)
        
        # Extract and format results
        analysis_results = result.get("analysis_results", {})
        
        # Display results in a formatted way
        display_results(analysis_results, text)
        
        # Save results if requested
        if save_results:
            save_analysis_results(analysis_results, thread_id)
        
        return analysis_results
        
    except Exception as e:
        print(f"❌ Error processing document: {str(e)}")
        return {"error": str(e)}

def display_results(results: Dict[str, Any], original_text: str):
    """Display analysis results in a formatted way"""
    print(f"\n{'='*60}")
    print("📊 ANALYSIS RESULTS")
    print('='*60)
    
    # Keywords
    keywords = results.get("keywords", [])
    if keywords:
        print(f"🔑 Keywords: {', '.join(keywords)}")
    else:
        print("🔑 Keywords: Unable to extract")
    
    # Summary
    summary = results.get("summary", "")
    if summary:
        quality = results.get("summary_quality", 0)
        print(f"📝 Summary: {summary}")
        quality_indicator = "🟢" if quality > 0.7 else "🟡" if quality > 0.4 else "🔴"
        print(f"   Quality Score: {quality:.2f}/1.00 {quality_indicator}")
    else:
        print("📝 Summary: Unable to generate")
    
    # Sentiment
    sentiment = results.get("sentiment", "")
    if sentiment:
        confidence = results.get("sentiment_confidence", 0)
        emoji = {"positive": "😊", "negative": "😞", "neutral": "😐"}.get(sentiment, "❓")
        confidence_indicator = "🟢" if confidence > 0.8 else "🟡" if confidence > 0.6 else "🔴"
        print(f"💭 Sentiment: {sentiment} {emoji} (confidence: {confidence:.2f} {confidence_indicator})")
    else:
        print("💭 Sentiment: Unable to analyze")
    
    # Review status
    review_status = results.get("review_status")
    if review_status:
        status_emoji = {"approved": "✅", "rejected": "❌", "skipped": "⏭️", "cancelled": "🚫"}.get(review_status, "❓")
        print(f"👤 Review Status: {review_status} {status_emoji}")
        
        # Add timestamp if available
        timestamp = results.get("review_timestamp")
        if timestamp:
            print(f"   Reviewed at: {timestamp}")
    
    # Word count and reading time
    word_count = len(original_text.split())
    reading_time = max(1, word_count // 200)  # Assume 200 words per minute
    print(f"📈 Text Stats: {word_count} words, ~{reading_time} min read")
    
    # Errors
    if "error" in results:
        print(f"⚠️  Error: {results['error']}")
    
    print('='*60)

def save_analysis_results(results: Dict[str, Any], thread_id: str):
    """Save analysis results to a JSON file"""
    try:
        filename = f"analysis_{thread_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Results saved to: {filename}")
    except Exception as e:
        print(f"⚠️  Could not save results: {str(e)}")

# ----------------------
# Main Execution
# ----------------------
if __name__ == "__main__":
    print("🚀 Document Analysis Bot - Enhanced Version")
    print("="*60)
    
    # Test cases
    test_documents = [
        {
            "text": "LangGraph's documentation provides exceptionally clear examples for state management and workflow orchestration",
            "id": "test_positive"
        },
        {
            "text": "This confidential report contains sensitive financial data including SSN 123-45-6789",
            "id": "test_sensitive"
        },
        {
            "text": "The weather today is okay, nothing special to report",
            "id": "test_neutral"
        },
        {
            "text": "This product is absolutely terrible and I hate everything about it",
            "id": "test_negative"
        }
    ]
    
    for doc in test_documents:
        results = process_document(doc["text"], doc["id"], save_results=False)
        if doc != test_documents[-1]:  # Add separator between tests
            print("\n" + "-"*60 + "\n")
    
    print("\n🎉 All tests completed!")