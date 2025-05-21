"""
Unit tests for the core tarot card functionality.

Tests cover TarotCard, TarotDeck, and TarotReading classes
to ensure proper functionality and reliability.
"""

import unittest
import tempfile
import os
import json
from unittest.mock import patch
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from tarot_core import TarotCard, TarotDeck, TarotReading


class TestTarotCard(unittest.TestCase):
    """Test cases for the TarotCard class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.card = TarotCard("The Fool", "New beginnings", "test.jpg", False)
        self.reversed_card = TarotCard("The Magician", "Manifestation", "test2.jpg", True)
    
    def test_card_initialization(self):
        """Test that cards are initialized correctly."""
        self.assertEqual(self.card.name, "The Fool")
        self.assertEqual(self.card.description, "New beginnings")
        self.assertEqual(self.card.image_file, "test.jpg")
        self.assertFalse(self.card.reversed)
    
    def test_card_flip(self):
        """Test that cards can be flipped correctly."""
        original_state = self.card.reversed
        self.card.flip()
        self.assertEqual(self.card.reversed, not original_state)
    
    def test_get_meaning_upright(self):
        """Test getting meaning for upright card."""
        meaning = self.card.get_meaning()
        self.assertIn("The Fool", meaning)
        self.assertIn("New beginnings", meaning)
        self.assertNotIn("Reversed", meaning)
    
    def test_get_meaning_reversed(self):
        """Test getting meaning for reversed card."""
        meaning = self.reversed_card.get_meaning()
        self.assertIn("The Magician", meaning)
        self.assertIn("Reversed", meaning)
        self.assertIn("opposite or blocked energy", meaning)
    
    def test_to_dict(self):
        """Test card serialization to dictionary."""
        card_dict = self.card.to_dict()
        expected_keys = {'name', 'description', 'image_file', 'reversed'}
        self.assertEqual(set(card_dict.keys()), expected_keys)
        self.assertEqual(card_dict['name'], "The Fool")
        self.assertEqual(card_dict['reversed'], False)
    
    def test_from_dict(self):
        """Test card deserialization from dictionary."""
        card_data = {
            'name': 'The Star',
            'description': 'Hope and guidance',
            'image_file': 'star.jpg',
            'reversed': True
        }
        card = TarotCard.from_dict(card_data)
        self.assertEqual(card.name, 'The Star')
        self.assertEqual(card.description, 'Hope and guidance')
        self.assertEqual(card.image_file, 'star.jpg')
        self.assertTrue(card.reversed)


class TestTarotDeck(unittest.TestCase):
    """Test cases for the TarotDeck class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.deck = TarotDeck()
    
    def test_deck_initialization(self):
        """Test that deck is initialized with correct number of cards."""
        # Should have 78 cards (22 Major + 56 Minor Arcana)
        self.assertEqual(len(self.deck.cards), 78)
    
    def test_deck_has_major_arcana(self):
        """Test that deck contains Major Arcana cards."""
        card_names = [card.name for card in self.deck.cards]
        major_arcana_cards = ["The Fool", "The Magician", "The World"]
        for card_name in major_arcana_cards:
            self.assertIn(card_name, card_names)
    
    def test_deck_has_minor_arcana(self):
        """Test that deck contains Minor Arcana cards."""
        card_names = [card.name for card in self.deck.cards]
        minor_arcana_samples = ["Ace of Cups", "King of Swords", "10 of Wands"]
        for card_name in minor_arcana_samples:
            self.assertIn(card_name, card_names)
    
    def test_shuffle_changes_order(self):
        """Test that shuffling changes card order."""
        original_order = [card.name for card in self.deck.cards]
        self.deck.shuffle()
        shuffled_order = [card.name for card in self.deck.cards]
        # Order should be different (extremely unlikely to be the same)
        self.assertNotEqual(original_order, shuffled_order)
    
    def test_draw_card(self):
        """Test drawing a single card."""
        initial_count = len(self.deck.cards)
        card = self.deck.draw_card()
        self.assertIsInstance(card, TarotCard)
        self.assertEqual(len(self.deck.cards), initial_count - 1)
    
    def test_draw_cards_multiple(self):
        """Test drawing multiple cards."""
        cards = self.deck.draw_cards(5)
        self.assertEqual(len(cards), 5)
        self.assertEqual(len(self.deck.cards), 73)  # 78 - 5
        for card in cards:
            self.assertIsInstance(card, TarotCard)
    
    def test_draw_cards_more_than_available(self):
        """Test drawing more cards than available."""
        # Draw almost all cards first
        self.deck.draw_cards(76)
        # Try to draw more than remaining
        cards = self.deck.draw_cards(5)
        self.assertEqual(len(cards), 2)  # Only 2 should remain
    
    def test_draw_from_empty_deck(self):
        """Test drawing from empty deck."""
        # Empty the deck
        self.deck.draw_cards(78)
        card = self.deck.draw_card()
        self.assertIsNone(card)
    
    def test_reset_deck(self):
        """Test resetting the deck."""
        self.deck.draw_cards(50)
        self.assertEqual(len(self.deck.cards), 28)
        self.deck.reset()
        self.assertEqual(len(self.deck.cards), 78)
    
    def test_remaining_cards(self):
        """Test getting remaining card count."""
        self.assertEqual(self.deck.remaining_cards(), 78)
        self.deck.draw_cards(10)
        self.assertEqual(self.deck.remaining_cards(), 68)


class TestTarotReading(unittest.TestCase):
    """Test cases for the TarotReading class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.reading = TarotReading()
    
    def test_single_card_reading(self):
        """Test single card reading."""
        result = self.reading.single_card_reading()
        self.assertEqual(result['type'], 'Single Card')
        self.assertEqual(len(result['cards']), 1)
        self.assertIn('interpretation', result)
        self.assertNotIn('error', result)
    
    def test_three_card_reading(self):
        """Test three card reading."""
        result = self.reading.three_card_reading()
        self.assertEqual(result['type'], 'Three Card (Past, Present, Future)')
        self.assertEqual(len(result['cards']), 3)
        self.assertIn('interpretation', result)
        self.assertIn('Past:', result['interpretation'])
        self.assertIn('Present:', result['interpretation'])
        self.assertIn('Future:', result['interpretation'])
    
    def test_celtic_cross_reading(self):
        """Test Celtic Cross reading."""
        result = self.reading.celtic_cross_reading()
        self.assertEqual(result['type'], 'Celtic Cross')
        self.assertEqual(len(result['cards']), 10)
        self.assertIn('interpretation', result)
        self.assertIn('Present Situation:', result['interpretation'])
        self.assertIn('Final Outcome:', result['interpretation'])
    
    def test_reading_with_insufficient_cards(self):
        """Test reading when not enough cards are available."""
        # Draw most cards
        self.reading.deck.draw_cards(75)
        result = self.reading.celtic_cross_reading()
        self.assertIn('error', result)
        self.assertIn('Not enough cards', result['error'])
    
    def test_get_reading_types(self):
        """Test getting available reading types."""
        types = self.reading.get_reading_types()
        expected_types = ["Single Card", "Three Card", "Celtic Cross"]
        self.assertEqual(types, expected_types)
    
    def test_save_reading(self):
        """Test saving a reading to file."""
        reading = self.reading.single_card_reading()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rdg') as f:
            temp_filename = f.name
        
        try:
            success = self.reading.save_reading(temp_filename, reading)
            self.assertTrue(success)
            
            # Verify file was created and contains correct data
            with open(temp_filename, 'r', encoding='utf-8') as f:
                saved_data = json.load(f)
            
            self.assertEqual(saved_data['type'], reading['type'])
            self.assertEqual(len(saved_data['cards']), len(reading['cards']))
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_load_reading(self):
        """Test loading a reading from file."""
        # Create test reading data
        test_reading = {
            'type': 'Single Card',
            'cards': [{'name': 'Test Card', 'description': 'Test', 'reversed': False}],
            'interpretation': 'Test interpretation'
        }
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rdg') as f:
            json.dump(test_reading, f)
            temp_filename = f.name
        
        try:
            loaded_reading = self.reading.load_reading(temp_filename)
            self.assertIsNotNone(loaded_reading)
            self.assertEqual(loaded_reading['type'], 'Single Card')
            self.assertEqual(loaded_reading['interpretation'], 'Test interpretation')
        
        finally:
            # Clean up
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)
    
    def test_load_nonexistent_file(self):
        """Test loading from nonexistent file."""
        result = self.reading.load_reading('nonexistent_file.rdg')
        self.assertIsNone(result)
    
    def test_readings_history(self):
        """Test that readings are added to history."""
        initial_history_length = len(self.reading.readings_history)
        
        self.reading.single_card_reading()
        self.assertEqual(len(self.reading.readings_history), initial_history_length + 1)
        
        self.reading.three_card_reading()
        self.assertEqual(len(self.reading.readings_history), initial_history_length + 2)


class TestTarotIntegration(unittest.TestCase):
    """Integration tests for the complete tarot system."""
    
    def test_full_reading_workflow(self):
        """Test a complete reading workflow."""
        reading_system = TarotReading()
        
        # Perform different types of readings
        single_reading = reading_system.single_card_reading()
        three_reading = reading_system.three_card_reading()
        
        # Verify readings are different
        self.assertNotEqual(single_reading['cards'], three_reading['cards'])
        
        # Verify history tracking
        self.assertEqual(len(reading_system.readings_history), 2)
    
    def test_card_reversal_mechanics(self):
        """Test that card reversal mechanics work correctly."""
        deck = TarotDeck()
        deck.shuffle()  # This should reverse some cards
        
        # Check if some cards are reversed
        reversed_cards = [card for card in deck.cards if card.reversed]
        # Should have some reversed cards (not all, not none)
        self.assertGreater(len(reversed_cards), 0)
        self.assertLess(len(reversed_cards), len(deck.cards))
    
    def test_save_load_roundtrip(self):
        """Test saving and loading maintains data integrity."""
        reading_system = TarotReading()
        original_reading = reading_system.celtic_cross_reading()
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.rdg') as f:
            temp_filename = f.name
        
        try:
            # Save and load
            reading_system.save_reading(temp_filename, original_reading)
            loaded_reading = reading_system.load_reading(temp_filename)
            
            # Verify data integrity
            self.assertEqual(original_reading['type'], loaded_reading['type'])
            self.assertEqual(len(original_reading['cards']), len(loaded_reading['cards']))
            
            # Check first card details
            orig_card = original_reading['cards'][0]
            loaded_card = loaded_reading['cards'][0]
            self.assertEqual(orig_card['name'], loaded_card['name'])
            self.assertEqual(orig_card['reversed'], loaded_card['reversed'])
        
        finally:
            if os.path.exists(temp_filename):
                os.unlink(temp_filename)


if __name__ == '__main__':
    unittest.main()