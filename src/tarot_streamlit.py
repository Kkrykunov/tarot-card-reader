"""
Tarot Card Reading Web Application

A Streamlit-based web application for tarot card readings.
Provides an interactive web interface for various types of tarot readings.
"""

import streamlit as st
import json
import io
from datetime import datetime
from typing import Dict, Optional
from tarot_core import TarotReading, TarotCard


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'tarot_reading' not in st.session_state:
        st.session_state.tarot_reading = TarotReading()
    if 'current_reading' not in st.session_state:
        st.session_state.current_reading = None
    if 'reading_history' not in st.session_state:
        st.session_state.reading_history = []


def display_card(card_data: Dict, position: Optional[str] = None) -> None:
    """Display a single tarot card with styling."""
    card = TarotCard.from_dict(card_data)
    
    with st.container():
        col1, col2 = st.columns([1, 3])
        
        with col1:
            # Card image placeholder (would show actual image if available)
            if card.image_file:
                st.image(card.image_file, width=100)
            else:
                st.markdown(
                    f"""
                    <div style="
                        width: 100px; 
                        height: 150px; 
                        background: {'#8B0000' if card.reversed else '#000080'}; 
                        border: 2px solid #FFD700;
                        border-radius: 10px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-weight: bold;
                        text-align: center;
                        margin-bottom: 10px;
                    ">
                        {'🔮' if not card.reversed else '🔮↕️'}
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
        
        with col2:
            if position:
                st.markdown(f"**{position}**")
            
            if card.reversed:
                st.markdown(f"**{card.name} (Reversed)**")
                st.markdown(f"*{card.description} - Consider the opposite or blocked energy.*")
            else:
                st.markdown(f"**{card.name}**")
                st.markdown(f"*{card.description}*")


def display_reading(reading: Dict) -> None:
    """Display a complete tarot reading."""
    st.markdown(f"## {reading['type']} Reading")
    st.markdown("---")
    
    # Display cards based on reading type
    if reading['type'] == "Single Card":
        display_card(reading['cards'][0])
    
    elif reading['type'] == "Three Card (Past, Present, Future)":
        positions = ["Past", "Present", "Future"]
        cols = st.columns(3)
        
        for i, (card_data, position) in enumerate(zip(reading['cards'], positions)):
            with cols[i]:
                st.markdown(f"### {position}")
                display_card(card_data)
    
    elif reading['type'] == "Celtic Cross":
        positions = [
            "Present Situation", "Challenge/Cross", "Distant Past/Foundation",
            "Recent Past", "Possible Outcome", "Near Future",
            "Your Approach", "External Influences", "Hopes and Fears", "Final Outcome"
        ]
        
        # Display in a grid layout
        for i in range(0, len(reading['cards']), 2):
            cols = st.columns(2)
            for j, col in enumerate(cols):
                if i + j < len(reading['cards']):
                    with col:
                        display_card(reading['cards'][i + j], positions[i + j])
    
    # Interpretation
    st.markdown("## Interpretation")
    st.markdown(reading['interpretation'])
    
    # Add to history
    if reading not in st.session_state.reading_history:
        reading['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.reading_history.append(reading)


def export_reading(reading: Dict) -> str:
    """Export reading to JSON format."""
    return json.dumps(reading, indent=2, ensure_ascii=False)


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="Tarot Card Reader",
        page_icon="🔮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    initialize_session_state()
    
    # Header
    st.title("🔮 Tarot Card Reader")
    st.markdown("*Discover insights through the ancient art of tarot*")
    st.markdown("---")
    
    # Sidebar for controls
    with st.sidebar:
        st.header("Reading Options")
        
        # Reading type selection
        reading_type = st.selectbox(
            "Select Reading Type:",
            ["Single Card", "Three Card", "Celtic Cross"],
            help="Choose the type of tarot reading you'd like to perform"
        )
        
        # Draw cards button
        if st.button("🎴 Draw Cards", type="primary", use_container_width=True):
            try:
                if reading_type == "Single Card":
                    reading = st.session_state.tarot_reading.single_card_reading()
                elif reading_type == "Three Card":
                    reading = st.session_state.tarot_reading.three_card_reading()
                elif reading_type == "Celtic Cross":
                    reading = st.session_state.tarot_reading.celtic_cross_reading()
                
                if "error" in reading:
                    st.error(reading["error"])
                else:
                    st.session_state.current_reading = reading
                    st.rerun()
            
            except Exception as e:
                st.error(f"Failed to draw cards: {str(e)}")
        
        # New reading button
        if st.button("🔄 New Reading", use_container_width=True):
            st.session_state.tarot_reading = TarotReading()
            st.session_state.current_reading = None
            st.rerun()
        
        st.markdown("---")
        
        # Reading history
        if st.session_state.reading_history:
            st.header("Reading History")
            
            for i, historical_reading in enumerate(reversed(st.session_state.reading_history[-5:])):
                timestamp = historical_reading.get('timestamp', 'Unknown time')
                if st.button(f"{historical_reading['type']} - {timestamp}", key=f"history_{i}"):
                    st.session_state.current_reading = historical_reading
                    st.rerun()
        
        st.markdown("---")
        
        # Export functionality
        if st.session_state.current_reading:
            st.header("Export Reading")
            
            reading_json = export_reading(st.session_state.current_reading)
            st.download_button(
                label="📥 Download as JSON",
                data=reading_json,
                file_name=f"tarot_reading_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        
        # File upload for loading readings
        st.header("Import Reading")
        uploaded_file = st.file_uploader(
            "Upload a reading file",
            type=['json', 'rdg'],
            help="Upload a previously saved tarot reading"
        )
        
        if uploaded_file is not None:
            try:
                content = uploaded_file.read().decode('utf-8')
                loaded_reading = json.loads(content)
                st.session_state.current_reading = loaded_reading
                st.success("Reading loaded successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Failed to load reading: {str(e)}")
    
    # Main content area
    if st.session_state.current_reading:
        display_reading(st.session_state.current_reading)
    else:
        # Welcome message
        st.markdown(
            """
            ## Welcome to the Tarot Card Reader! 🌟
            
            This application offers three types of tarot readings:
            
            ### 🃏 Single Card Reading
            Perfect for daily guidance or when you need a quick insight into a specific question.
            
            ### 🃏🃏🃏 Three Card Reading
            Explores the **Past**, **Present**, and **Future** aspects of your situation.
            
            ### 🃏✨ Celtic Cross Reading
            A comprehensive 10-card spread that provides deep insights into your current situation,
            challenges, influences, and potential outcomes.
            
            ---
            
            **To get started:**
            1. Select a reading type from the sidebar
            2. Click "Draw Cards" to begin your reading
            3. Explore the meaning of each card drawn
            
            *Each reading uses a complete 78-card tarot deck with both Major and Minor Arcana.*
            """
        )
        
        # Display some cards as preview
        st.markdown("### Example Cards from the Deck")
        
        # Create example cards for display
        example_cards = [
            {"name": "The Fool", "description": "New beginnings, spontaneity, innocence", "reversed": False},
            {"name": "The Star", "description": "Hope, faith, purpose, renewal, spirituality", "reversed": True},
            {"name": "Queen of Cups", "description": "Queen energy in the realm of emotions, intuition, relationships, spirituality", "reversed": False}
        ]
        
        cols = st.columns(3)
        for i, card_data in enumerate(example_cards):
            with cols[i]:
                display_card(card_data)
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center'>
            <p><em>Remember: Tarot readings are for entertainment and self-reflection purposes. 
            Trust your intuition and use the insights as guidance for your personal journey.</em></p>
        </div>
        """, 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()