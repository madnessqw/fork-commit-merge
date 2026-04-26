#!/usr/bin/env python3
"""
AI Receptionist for Small Businesses
A complete phone/chat receptionist system for local businesses
Trending opportunity: Hacker News #2 today - "AI Receptionist for Luxury Mechanic Shop"

Features:
- Appointment scheduling via natural language
- FAQ handling with custom knowledge base
- Call transcription and summarization
- Integration with Google Calendar
- Multi-channel: Phone (Twilio), WhatsApp, Telegram

Usage:
    python ai_receptionist.py --setup
    python ai_receptionist.py --demo
    python ai_receptionist.py --run

Author: UniverseCreator
License: MIT
"""

import json
import sqlite3
import re
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse


@dataclass
class Appointment:
    id: Optional[int]
    customer_name: str
    customer_phone: str
    service_type: str
    datetime: str
    duration_minutes: int
    notes: str
    status: str
    created_at: str


class AIReceptionist:
    """AI-powered receptionist for small businesses."""
    
    def __init__(self, business_name: str = "Your Business", db_path: str = "receptionist.db"):
        self.business_name = business_name
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        """Initialize SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                customer_phone TEXT NOT NULL,
                service_type TEXT NOT NULL,
                datetime TEXT NOT NULL,
                duration_minutes INTEGER DEFAULT 60,
                notes TEXT,
                status TEXT DEFAULT 'scheduled',
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS faq (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                answer TEXT NOT NULL,
                keywords TEXT,
                category TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_phone TEXT NOT NULL,
                message TEXT NOT NULL,
                response TEXT NOT NULL,
                intent TEXT,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def process_message(self, customer_phone: str, message: str) -> str:
        """Process incoming message and return AI response."""
        intent = self._classify_intent(message)
        
        if intent == "book_appointment":
            response = self._handle_booking_intent(customer_phone, message)
        elif intent == "check_availability":
            response = self._handle_availability_check(message)
        elif intent == "faq_question":
            response = self._handle_faq(message)
        elif intent == "cancel_appointment":
            response = self._handle_cancellation(customer_phone, message)
        elif intent == "reschedule":
            response = self._handle_reschedule(customer_phone, message)
        else:
            response = self._handle_general_inquiry(message)
            
        self._log_conversation(customer_phone, message, response, intent)
        return response
        
    def _classify_intent(self, message: str) -> str:
        """Classify customer intent from message."""
        msg_lower = message.lower()
        
        booking_keywords = ['book', 'appointment', 'schedule', 'reserve', 'slot', 'available', 'when can i', 'i want to']
        cancel_keywords = ['cancel', 'reschedule', 'change', 'move', 'can\'t make it', 'different time']
        faq_keywords = ['hours', 'price', 'cost', 'location', 'address', 'open', 'close', 'service', 'what do you', 'how much']
        
        if any(k in msg_lower for k in booking_keywords):
            return "book_appointment"
        if any(k in msg_lower for k in cancel_keywords):
            return "cancel_appointment"
        if any(k in msg_lower for k in faq_keywords):
            return "faq_question"
            
        return "general"
        
    def _handle_booking_intent(self, customer_phone: str, message: str) -> str:
        """Handle appointment booking intent."""
        extracted_time = self._extract_datetime(message)
        
        if not extracted_time:
            return f"I'd be happy to book an appointment for you at {self.business_name}. What date and time works best? We're open Monday-Saturday 9AM-6PM."
            
        if self._is_slot_available(extracted_time):
            return f"Great! I can book you in for {extracted_time}. What service do you need? (e.g., consultation, repair, maintenance)"
        else:
            alternatives = self._get_available_slots(extracted_time[:10], limit=3)
            alt_text = ", ".join(alternatives)
            return f"That time isn't available. Here are some alternatives: {alt_text}. Would any of these work?"
            
    def _handle_availability_check(self, message: str) -> str:
        """Check and report availability."""
        date = self._extract_date(message)
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
            
        slots = self._get_available_slots(date, limit=5)
        if slots:
            return f"We have availability on {date} at: {', '.join(slots)}. Would you like to book one of these?"
        else:
            return f"We're fully booked on {date}. Would you like to see availability for the next few days?"
            
    def _handle_faq(self, message: str) -> str:
        """Answer FAQ questions."""
        answer = self._search_faq(message)
        if answer:
            return answer
        return f"I'm not sure about that. Let me connect you with someone at {self.business_name} who can help. They'll call you back shortly."
        
    def _handle_cancellation(self, customer_phone: str, message: str) -> str:
        """Handle appointment cancellation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE appointments SET status = 'cancelled' WHERE customer_phone = ? AND status = 'scheduled'",
            (customer_phone,)
        )
        conn.commit()
        conn.close()
        return "Your appointment has been cancelled. Is there anything else I can help you with?"
        
    def _handle_reschedule(self, customer_phone: str, message: str) -> str:
        """Handle rescheduling."""
        return "I can help you reschedule. What new date and time would work for you?"
        
    def _handle_general_inquiry(self, message: str) -> str:
        """Handle general inquiries."""
        return f"Thank you for contacting {self.business_name}. I'm the AI receptionist. I can help you book appointments, check availability, or answer questions. What would you like to do?"
        
    def _extract_datetime(self, message: str) -> Optional[str]:
        """Extract datetime from natural language."""
        today = datetime.now()
        
        if 'tomorrow' in message.lower():
            date = today + timedelta(days=1)
            time_match = re.search(r'(\d{1,2}):?(\d{2})?\s*(am|pm)?', message.lower())
            if time_match:
                hour = int(time_match.group(1))
                minute