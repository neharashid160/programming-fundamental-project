"""
CapGenius Caption Engine - Professional Backend for AI-powered Instagram Caption Generation
Uses Grok Cloud API to generate captions, hashtags, and engagement scoring.
Production-grade backend with comprehensive error handling and validation.
"""

import json
import os
from datetime import datetime
from pathlib import Path
import pyperclip
import requests
from openai import OpenAI


def test_api_key(api_key):
    """
    Test if the API key is valid and can connect to Grok API.
    
    Args:
        api_key (str): Grok Cloud API key
    
    Returns:
        tuple: (success: bool, message: str)
    """
    try:
        if not api_key or not api_key.strip():
            return (False, "API key is empty")
        
        # Strip any whitespace from API key
        api_key = api_key.strip()
        
        # Initialize Grok client
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Simple test prompt
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": "Say 'API connection successful' in one sentence only."}
            ],
            max_tokens=50
        )
        
        if response and response.choices and response.choices[0].message.content:
            return (True, "API key is valid and connected to Grok!")
        else:
            return (False, "API returned empty response - key may be invalid")
            
    except Exception as e:
        error_str = str(e)
        print(f"DEBUG: Full error: {error_str}")  # Debug output
        error_lower = error_str.lower()
        
        if "401" in error_str or "authentication" in error_lower or "invalid" in error_lower or "unauthorized" in error_lower or "api_key" in error_lower:
            return (False, f"❌ Invalid API key or authentication failed. Error: {error_str[:100]}")
        elif "quota" in error_lower or "rate" in error_lower:
            return (False, "⏱️ API quota exceeded - please wait a moment and try again")
        elif "connection" in error_lower or "network" in error_lower or "timeout" in error_lower:
            return (False, "🌐 Network connection error - check your internet connection")
        else:
            return (False, f"API connection failed: {error_str[:150]}")


def generate_caption(keywords, tone, num_variations, api_key):
    """
    Generate Instagram captions using Grok Cloud API.
    
    Args:
        keywords (str): Description or keywords for the caption
        tone (str): Tone of captions (Casual, Professional, Humorous, Inspirational)
        num_variations (int): Number of caption variations to generate (1-5)
        api_key (str): Grok Cloud API key
    
    Returns:
        list: List of generated caption strings
    
    Raises:
        ValueError: If API key is empty or keywords are empty
        Exception: If API call fails or connection error occurs
    """
    try:
        # Validate inputs
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")
        if not keywords or not keywords.strip():
            raise ValueError("Keywords cannot be empty")
        if num_variations < 1 or num_variations > 5:
            raise ValueError("Number of variations must be between 1 and 5")
        
        # Initialize Grok client (strip whitespace from API key)
        api_key = api_key.strip()
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
            timeout=30.0  # 30 second timeout
        )
        
        # Create the prompt for caption generation
        prompt = f"""Generate {num_variations} Instagram captions with a {tone} tone based on these keywords: "{keywords}"
        
        Requirements:
        - Each caption should be unique and engaging
        - Keep each caption under 280 characters
        - Make them suitable for Instagram
        - Use relevant emojis where appropriate
        - Do not include hashtags in the captions
        
        Format your response as a numbered list (1., 2., etc.)"""
        
        # Call Grok API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        # Check if response is empty
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("API returned empty response")
        
        response_text = response.choices[0].message.content
        
        # Parse the response into a list of captions
        captions = []
        lines = response_text.strip().split('\n')
        
        for line in lines:
            # Remove numbering and clean up the caption
            line = line.strip()
            if line and line[0].isdigit():
                # Remove the number and period/dot at the beginning
                caption = line.split('.', 1)[1].strip() if '.' in line else line
            else:
                caption = line
            
            if caption:
                captions.append(caption)
        
        return captions if captions else [response_text]
    
    except ValueError as ve:
        raise ValueError(f"Input validation error: {str(ve)}")
    except Exception as e:
        raise Exception(f"Grok API error: {str(e)}")


def suggest_hashtags(keywords, tone, api_key):
    """
    Generate highly relevant Instagram hashtags using Grok Cloud API.
    Mix of popular, niche, and branded hashtags optimized for the given tone.
    
    Args:
        keywords (str): Description or keywords for hashtag generation
        tone (str): Tone of content (Casual, Professional, Humorous, Inspirational)
        api_key (str): Grok Cloud API key
    
    Returns:
        list: List of 15 relevant hashtags (without # symbol)
    
    Raises:
        ValueError: If API key or keywords are empty
        Exception: If API call fails
    """
    try:
        # Validate inputs
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")
        if not keywords or not keywords.strip():
            raise ValueError("Keywords cannot be empty")
        
        # Initialize Grok client (strip whitespace from API key)
        api_key = api_key.strip()
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Create the prompt for hashtag generation with tone awareness
        prompt = f"""Generate 15 highly relevant Instagram hashtags for {tone} content related to: "{keywords}"
        
        Requirements:
        - Mix of popular hashtags (1M-10M posts), niche hashtags (100K-1M), and micro hashtags (10K-100K)
        - Include branded and trending hashtags when relevant
        - Optimize for {tone} tone and audience
        - Return only the hashtag words (without # symbol)
        - One hashtag per line
        - No explanations, numbering, or category labels
        - No duplicate hashtags"""
        
        # Call Grok API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=500
        )
        
        # Check if response is empty
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("API returned empty response for hashtags")
        
        response_text = response.choices[0].message.content
        
        # Parse the response into a list of hashtags
        hashtags = []
        lines = response_text.strip().split('\n')
        
        for line in lines:
            # Clean up the hashtag
            hashtag = line.strip().lstrip('#').strip()
            # Remove numbering if present
            if hashtag and hashtag[0].isdigit():
                hashtag = hashtag.split('.', 1)[1].strip() if '.' in hashtag else ''
            if hashtag:
                hashtags.append(hashtag)
        
        # Return first 15 hashtags
        return hashtags[:15]
    
    except ValueError as ve:
        raise ValueError(f"Input validation error: {str(ve)}")
    except Exception as e:
        raise Exception(f"Failed to generate hashtags: {str(e)}")


def get_caption_score(caption, api_key):
    """
    Score a caption's engagement potential using Grok Cloud API.
    Analyzes hook, emojis, call-to-action, and overall engagement appeal.
    
    Args:
        caption (str): The caption text to score
        api_key (str): Grok Cloud API key
    
    Returns:
        tuple: (score (int 1-10), reason (str)) - e.g., (8, "Strong hook and clear CTA")
    
    Raises:
        ValueError: If caption or API key is empty
        Exception: If API call fails
    """
    try:
        # Validate inputs
        if not caption or not caption.strip():
            raise ValueError("Caption cannot be empty")
        if not api_key or not api_key.strip():
            raise ValueError("API key cannot be empty")
        
        # Initialize Grok client (strip whitespace from API key)
        api_key = api_key.strip()
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        # Create the prompt for caption scoring
        prompt = f"""Rate this Instagram caption for engagement potential on a scale of 1-10.
        
Caption: "{caption}"

Consider:
- Hook strength (attention-grabbing opening)
- Use of emojis (enhances visual appeal)
- Call-to-action (encourages engagement)
- Length (optimal for platform)
- Authenticity and relatability
- Hashtag placement (if any)

RESPOND WITH ONLY:
[SCORE]/10 — [ONE-LINE REASON]

Example:
8/10 — Strong hook with relatable question and clear CTA
"""
        
        # Call Grok API
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )
        
        if not response.choices or not response.choices[0].message.content:
            raise ValueError("API returned empty response for scoring")
        
        response_text = response.choices[0].message.content.strip()
        
        try:
            # Extract score and reason
            if "—" in response_text:
                score_part, reason_part = response_text.split("—", 1)
                score_str = score_part.strip().split("/")[0].strip()
                score = int(score_str)
                reason = reason_part.strip()
            else:
                # Fallback parsing
                score_str = response_text.split("/")[0].strip()
                score = int(score_str)
                reason = "Engagement score calculated"
            
            # Ensure score is in valid range
            score = max(1, min(10, score))
            
            return (score, reason)
        
        except (ValueError, IndexError):
            # If parsing fails, return a default score
            return (7, "Score generated - see details in response")
    
    except ValueError as ve:
        raise ValueError(f"Input validation error: {str(ve)}")
    except Exception as e:
        raise Exception(f"Failed to score caption: {str(e)}")


def save_to_history(caption, hashtags, tone, filepath="data/history.json"):
    """
    Save a caption with hashtags, tone, and timestamp to history.json.
    Creates the file and data/ folder if they don't exist.
    
    Args:
        caption (str): The caption text to save
        hashtags (list): List of hashtag strings (without # symbol)
        tone (str): The tone of the caption (Casual, Professional, etc.)
        filepath (str): Path to the history.json file
    
    Raises:
        Exception: If file I/O operation fails
    """
    try:
        # Validate input
        if not caption or not caption.strip():
            raise ValueError("Caption cannot be empty")
        
        # Create data directory if it doesn't exist
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        
        # Load existing history or create new list
        history = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    history = json.load(f)
            except (json.JSONDecodeError, IOError):
                history = []
        
        # Create new entry with timestamp and metadata
        entry = {
            "caption": caption,
            "hashtags": hashtags if isinstance(hashtags, list) else [],
            "tone": tone,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Append to history
        history.append(entry)
        
        # Save updated history
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    
    except IOError as ie:
        raise Exception(f"File I/O error: {str(ie)}")
    except Exception as e:
        raise Exception(f"Failed to save caption to history: {str(e)}")


def load_history(filepath="data/history.json"):
    """
    Load all saved captions from history.json.
    
    Args:
        filepath (str): Path to the history.json file
    
    Returns:
        list: List of dictionaries with 'caption' and 'timestamp' keys
              Returns empty list if file doesn't exist
    
    Raises:
        Exception: If file read or JSON parsing fails
    """
    try:
        # Return empty list if file doesn't exist
        if not os.path.exists(filepath):
            return []
        
        # Read and parse the JSON file
        with open(filepath, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        return history if isinstance(history, list) else []
    
    except json.JSONDecodeError as je:
        raise Exception(f"Invalid JSON in history file: {str(je)}")
    except IOError as ie:
        raise Exception(f"File I/O error: {str(ie)}")
    except Exception as e:
        raise Exception(f"Failed to load history: {str(e)}")


def clear_history(filepath="data/history.json"):
    """
    Clear all saved captions from history.json.
    
    Args:
        filepath (str): Path to the history.json file
    
    Raises:
        Exception: If file operation fails
    """
    try:
        # Create empty history
        if os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    except IOError as ie:
        raise Exception(f"File I/O error: {str(ie)}")
    except Exception as e:
        raise Exception(f"Failed to clear history: {str(e)}")


def copy_to_clipboard(text):
    """
    Copy text to system clipboard using pyperclip.
    
    Args:
        text (str): Text to copy to clipboard
    
    Raises:
        Exception: If clipboard operation fails
    """
    try:
        # Validate input
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Copy to clipboard
        pyperclip.copy(text)
    
    except Exception as e:
        raise Exception(f"Failed to copy to clipboard: {str(e)}")
