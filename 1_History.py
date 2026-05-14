"""
CapGenius - Caption History Page
Pure Streamlit application with no custom CSS, HTML, or JavaScript.
Uses native Streamlit components only.
"""

import streamlit as st
from caption_engine import load_history, clear_history


def main():
    """
    Main Streamlit application entry point for History page.
    Pure Streamlit components only - no custom CSS, HTML, or JavaScript.
    """
    
    # Page configuration
    st.set_page_config(
        page_title="Caption History",
        page_icon="📋",
        layout="wide"
    )
    
    # Header
    st.title("📋 Caption History")
    st.caption("All your saved captions in one place")
    st.divider()
    
    # Load history from caption_engine
    try:
        history = load_history()
    except Exception as e:
        st.error(f"Failed to load history: {str(e)}")
        history = []
    
    # Check if history is empty
    if not history:
        st.info("No captions saved yet. Go to Home and generate some! ✨")
    else:
        # Show total saved captions metric
        st.metric("Total Saved Captions", len(history))
        st.divider()
        
        # Display each saved caption
        for i, entry in enumerate(reversed(history)):
            caption_text = entry.get('caption', 'No text')
            hashtags = entry.get('hashtags', [])
            tone = entry.get('tone', 'Unknown')
            timestamp = entry.get('timestamp', 'Unknown time')
            
            with st.container(border=True):
                # Three columns layout
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.write(caption_text)
                    if hashtags:
                        hashtags_str = " ".join([f"#{tag}" for tag in hashtags])
                        st.caption(hashtags_str)
                
                with col2:
                    st.caption(f"🎨 {tone}")
                    st.caption(f"🕐 {timestamp}")
                
                with col3:
                    # Delete button for individual entry
                    if st.button("🗑️", key=f"del_{i}"):
                        try:
                            # Remove the entry from history
                            updated_history = [h for h in history if h != entry]
                            # Save updated history
                            import json
                            import os
                            from datetime import datetime
                            
                            directory = os.path.dirname("data/history.json")
                            if directory and not os.path.exists(directory):
                                os.makedirs(directory)
                            
                            with open("data/history.json", 'w', encoding='utf-8') as f:
                                json.dump(updated_history, f, indent=2, ensure_ascii=False)
                            
                            st.success("✅ Caption deleted!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"Failed to delete: {str(e)}")
        
        st.divider()
        
        # Clear all history button
        if st.button("🗑️ Clear All History", type="secondary"):
            st.warning("⚠️ Are you sure you want to delete all saved captions?")
            if st.checkbox("Confirm deletion"):
                try:
                    clear_history()
                    st.success("✅ All history cleared!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Failed to clear history: {str(e)}")


if __name__ == "__main__":
    main()
