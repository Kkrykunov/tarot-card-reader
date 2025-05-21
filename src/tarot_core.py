"""
Core Tarot Card System

This module contains the fundamental classes for a tarot card reading application:
- TarotCard: Represents individual tarot cards with names, descriptions, and reversed states
- TarotDeck: Manages the complete deck of 78 tarot cards (Major and Minor Arcana)
- TarotReading: Handles different types of card readings and interpretations
"""

import random
import json
from typing import List, Dict, Optional


class TarotCard:
    """Represents a single tarot card with its properties and state."""
    
    def __init__(self, name: str, description: str, image_file: Optional[str] = None, reversed: bool = False):
        """
        Initialize a tarot card.
        
        Args:
            name: The name of the tarot card
            description: The meaning/description of the card
            image_file: Optional path to card image file
            reversed: Whether the card is in reversed position
        """
        self.name = name
        self.description = description
        self.image_file = image_file
        self.reversed = reversed
    
    def flip(self) -> None:
        """Flip the card to change its reversed state."""
        self.reversed = not self.reversed
    
    def get_meaning(self) -> str:
        """Get the card's meaning based on its orientation."""
        if self.reversed:
            return f"{self.name} (Reversed): {self.description} - Consider the opposite or blocked energy."
        return f"{self.name}: {self.description}"
    
    def to_dict(self) -> Dict:
        """Convert card to dictionary for serialization."""
        return {
            'name': self.name,
            'description': self.description,
            'image_file': self.image_file,
            'reversed': self.reversed
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'TarotCard':
        """Create card from dictionary."""
        return cls(
            name=data['name'],
            description=data['description'],
            image_file=data.get('image_file'),
            reversed=data.get('reversed', False)
        )


class TarotDeck:
    """Manages the complete deck of tarot cards."""
    
    def __init__(self):
        """Initialize the complete tarot deck with all 78 cards."""
        self.cards = []
        self._create_deck()
    
    def _create_deck(self) -> None:
        """Create the complete tarot deck with Major and Minor Arcana."""
        # Major Arcana (22 cards)
        major_arcana = [
            ("The Fool", "New beginnings, spontaneity, innocence"),
            ("The Magician", "Manifestation, resourcefulness, power"),
            ("The High Priestess", "Intuition, sacred knowledge, divine feminine"),
            ("The Empress", "Femininity, beauty, nature, abundance"),
            ("The Emperor", "Authority, structure, control, father-figure"),
            ("The Hierophant", "Spiritual wisdom, religious beliefs, conformity"),
            ("The Lovers", "Love, harmony, relationships, values alignment"),
            ("The Chariot", "Control, willpower, success, determination"),
            ("Strength", "Inner strength, bravery, compassion, focus"),
            ("The Hermit", "Soul searching, introspection, inner guidance"),
            ("Wheel of Fortune", "Good luck, karma, life cycles, destiny"),
            ("Justice", "Justice, fairness, truth, cause and effect"),
            ("The Hanged Man", "Suspension, restriction, letting go"),
            ("Death", "Endings, beginnings, change, transformation"),
            ("Temperance", "Balance, moderation, patience, purpose"),
            ("The Devil", "Shadow self, attachment, addiction, restriction"),
            ("The Tower", "Sudden change, upheaval, chaos, revelation"),
            ("The Star", "Hope, faith, purpose, renewal, spirituality"),
            ("The Moon", "Illusion, fear, anxiety, subconscious, intuition"),
            ("The Sun", "Optimism, fun, warmth, success, vitality"),
            ("Judgement", "Reflection, reckoning, awakening"),
            ("The World", "Completion, integration, accomplishment, travel")
        ]
        
        # Minor Arcana suits
        suits = ["Cups", "Wands", "Swords", "Pentacles"]
        suit_meanings = {
            "Cups": "emotions, intuition, relationships, spirituality",
            "Wands": "creativity, action, passion, career",
            "Swords": "thoughts, communication, conflict, intellect",
            "Pentacles": "material world, resources, money, career"
        }
        
        # Add Major Arcana
        for name, description in major_arcana:
            self.cards.append(TarotCard(name, description))
        
        # Add Minor Arcana (56 cards)
        for suit in suits:
            suit_meaning = suit_meanings[suit]
            
            # Number cards (Ace through 10)
            for i in range(1, 11):
                if i == 1:
                    name = f"Ace of {suit}"
                else:
                    name = f"{i} of {suit}"
                description = f"Represents {suit_meaning} at level {i}"
                self.cards.append(TarotCard(name, description))
            
            # Court cards
            court_cards = ["Page", "Knight", "Queen", "King"]
            for court in court_cards:
                name = f"{court} of {suit}"
                description = f"{court} energy in the realm of {suit_meaning}"
                self.cards.append(TarotCard(name, description))
    
    def shuffle(self) -> None:
        """Shuffle the deck and randomly reverse some cards."""
        random.shuffle(self.cards)
        for card in self.cards:
            if random.choice([True, False]):
                card.flip()
    
    def draw_card(self) -> Optional[TarotCard]:
        """Draw a card from the deck."""
        if self.cards:
            return self.cards.pop()
        return None
    
    def draw_cards(self, count: int) -> List[TarotCard]:
        """Draw multiple cards from the deck."""
        drawn_cards = []
        for _ in range(min(count, len(self.cards))):
            card = self.draw_card()
            if card:
                drawn_cards.append(card)
        return drawn_cards
    
    def reset(self) -> None:
        """Reset the deck to full 78 cards."""
        self.cards.clear()
        self._create_deck()
    
    def remaining_cards(self) -> int:
        """Get the number of remaining cards in the deck."""
        return len(self.cards)


class TarotReading:
    """Handles different types of tarot card readings."""
    
    def __init__(self):
        """Initialize a new tarot reading session."""
        self.deck = TarotDeck()
        self.readings_history = []
    
    def single_card_reading(self) -> Dict:
        """Perform a single card reading."""
        self.deck.shuffle()
        card = self.deck.draw_card()
        
        if not card:
            return {"error": "No cards available"}
        
        reading = {
            "type": "Single Card",
            "cards": [card.to_dict()],
            "interpretation": f"Today's guidance: {card.get_meaning()}"
        }
        
        self.readings_history.append(reading)
        return reading
    
    def three_card_reading(self) -> Dict:
        """Perform a three card reading (Past, Present, Future)."""
        self.deck.shuffle()
        cards = self.deck.draw_cards(3)
        
        if len(cards) < 3:
            return {"error": "Not enough cards available"}
        
        positions = ["Past", "Present", "Future"]
        interpretation = []
        
        for i, card in enumerate(cards):
            interpretation.append(f"{positions[i]}: {card.get_meaning()}")
        
        reading = {
            "type": "Three Card (Past, Present, Future)",
            "cards": [card.to_dict() for card in cards],
            "interpretation": "\n".join(interpretation)
        }
        
        self.readings_history.append(reading)
        return reading
    
    def celtic_cross_reading(self) -> Dict:
        """Perform a Celtic Cross reading (10 cards)."""
        self.deck.shuffle()
        cards = self.deck.draw_cards(10)
        
        if len(cards) < 10:
            return {"error": "Not enough cards for Celtic Cross reading"}
        
        positions = [
            "Present Situation",
            "Challenge/Cross",
            "Distant Past/Foundation",
            "Recent Past",
            "Possible Outcome",
            "Near Future",
            "Your Approach",
            "External Influences",
            "Hopes and Fears",
            "Final Outcome"
        ]
        
        interpretation = []
        for i, card in enumerate(cards):
            interpretation.append(f"{positions[i]}: {card.get_meaning()}")
        
        reading = {
            "type": "Celtic Cross",
            "cards": [card.to_dict() for card in cards],
            "interpretation": "\n".join(interpretation)
        }
        
        self.readings_history.append(reading)
        return reading
    
    def save_reading(self, filename: str, reading: Dict) -> bool:
        """Save a reading to a file."""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(reading, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Error saving reading: {e}")
            return False
    
    def load_reading(self, filename: str) -> Optional[Dict]:
        """Load a reading from a file."""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading reading: {e}")
            return None
    
    def get_reading_types(self) -> List[str]:
        """Get available reading types."""
        return ["Single Card", "Three Card", "Celtic Cross"]