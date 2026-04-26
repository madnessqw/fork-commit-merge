#!/usr/bin/env python3
"""
AI Receptionist for Small Businesses - Complete Professional Version
A complete phone/chat receptionist system for local businesses

Features:
- Appointment scheduling via natural language
- FAQ handling with custom knowledge base
- Call transcription and summarization
- Multi-channel: WhatsApp, Telegram, SMS
- Google Calendar integration ready
- Web dashboard for business owners

Usage:
    python ai_receptionist_complete.py --setup
    python ai_receptionist_complete.py --demo
    python ai_receptionist_complete.py --run

Author: UniverseCreator
License: MIT
Version: 1.0.0
"""

import json
import sqlite3
import re
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from dataclasses import dataclass, asdict
from pathlib import Path
import argparse
import random


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
        self.services = [
            "consultation", "meeting", "appointment", 
            "service", "repair", "maintenance", "checkup"
        ]
        self.business_hours = {
            "monday": ("09:00", "18:00"),
            "tuesday": ("09:00", "18:00"),
            "wednesday": ("09:00", "18:00"),
            "thursday": ("09:00", "18:00"),
            "friday": ("09:00", "18:00"),
            "saturday": ("10:00", "16:00"),
            "sunday": None
        }
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
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT UNIQUE NOT NULL,
                email TEXT,
                preferences TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
    def process_message(self, customer_phone: str, message: str, customer_name: str = None) -> str:
        """Process incoming message and return AI response."""
        intent = self._classify_intent(message)
        
        # Store/update customer
        if customer_name:
            self._store_customer(customer_name, customer_phone)
        
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
        elif intent == "my_appointments":
            response = self._handle_my_appointments(customer_phone)
        else:
            response = self._handle_general_inquiry(message)
            
        self._log_conversation(customer_phone, message, response, intent)
        return response
        
    def _classify_intent(self, message: str) -> str:
        """Classify customer intent from message."""
        msg_lower = message.lower()
        
        booking_keywords = ['book', 'appointment', 'schedule', 'reserve', 'slot', 
                           'available', 'when can i', 'i want to', 'i need to', 'can i get']
        cancel_keywords = ['cancel', 'delete', 'remove', 'can\'t make it']
        reschedule_keywords = ['reschedule', 'change', 'move', 'different time', 'another time']
        faq_keywords = ['hours', 'price', 'cost', 'location', 'address', 'open', 
                       'close', 'service', 'what do you', 'how much', 'where are you']
        my_appt_keywords = ['my appointment', 'my booking', 'when is my', 'what time is my']
        
        if any(k in msg_lower for k in cancel_keywords):
            return "cancel_appointment"
        if any(k in msg_lower for k in reschedule_keywords):
            return "reschedule"
        if any(k in msg_lower for k in my_appt_keywords):
            return "my_appointments"
        if any(k in msg_lower for k in booking_keywords):
            return "book_appointment"
        if any(k in msg_lower for k in faq_keywords):
            return "faq_question"
            
        return "general"
        
    def _handle_booking_intent(self, customer_phone: str, message: str) -> str:
        """Handle appointment booking intent."""
        extracted_time = self._extract_datetime(message)
        service = self._extract_service(message)
        
        if not extracted_time:
            return (f"I'd be happy to book an appointment for you at {self.business_name}. "
                    f"What date and time works best? We're open Monday-Friday 9AM-6PM, "
                    f"Saturday 10AM-4PM.")
        
        # Check if it's during business hours
        if not self._is_business_hours(extracted_time):
            return (f"I'm sorry, that time is outside our business hours. "
                    f"We're open Monday-Friday 9AM-6PM, Saturday 10AM-4PM. "
                    f"Would you like to see available slots?")
            
        if self._is_slot_available(extracted_time):
            if service:
                self._book_appointment(customer_phone, extracted_time, service)
                return (f"Perfect! I've booked your {service} appointment for {extracted_time}. "
                        f"We look forward to seeing you at {self.business_name}! "
                        f"Reply CANCEL if you need to cancel.")
            else:
                return (f"Great! I can book you in for {extracted_time}. "
                        f"What service do you need? (e.g., consultation, repair, maintenance)")
        else:
            alternatives = self._get_available_slots(extracted_time[:10], limit=3)
            if alternatives:
                alt_text = ", 