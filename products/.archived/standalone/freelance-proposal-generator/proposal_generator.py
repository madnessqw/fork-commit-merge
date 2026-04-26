#!/usr/bin/env python3
"""
Freelance Proposal Generator
Generates customized, high-converting proposals for Upwork/Fiverr jobs
Product #31 - Built by UniverseCreator
"""

import json
import re
from datetime import datetime
from pathlib import Path

# Proposal templates by category
TEMPLATES = {
    "web_development": {
        "opening": """Hi {client_name},

I came across your posting for {job_title} and immediately knew I was the right fit. With {experience_years}+ years of experience in {primary_skill}, I've helped {client_count}+ clients achieve {typical_result}.

**Why I'm Different:**
Unlike other freelancers who just "get the job done," I focus on {unique_value_prop}. My approach combines technical excellence with business understanding - I don't just write code, I solve problems.""",
        
        "body": """
**Here's exactly how I'll deliver {deliverable}:**

✅ **Phase 1: Discovery & Planning** ({phase1_duration})
   - Deep dive into your requirements
   - Technical architecture design
   - Timeline and milestone planning

✅ **Phase 2: Development** ({phase2_duration})
   - Clean, maintainable code following best practices
   - Regular progress updates every {update_frequency}
   - Rigorous testing at each stage

✅ **Phase 3: Delivery & Support** ({phase3_duration})
   - Complete documentation
   - Deployment assistance
   - {support_duration} of post-launch support

**Recent Similar Projects:**
{portfolio_examples}

**My Tech Stack:**
{tech_stack}

**What You Get:**
{deliverables_list}
""",
        
        "closing": """
**Ready to start?** 

I'm available to begin immediately and can have {first_deliverable} ready by {first_deadline}.

Let's schedule a quick 15-minute call to discuss your project in detail. I'm confident I can exceed your expectations.

Best regards,
{my_name}
{my_title}

P.S. Check out my portfolio: {portfolio_url}
"""
    },
    
    "automation_scripting": {
        "opening": """Hi {client_name},

Your project for {job_title} caught my attention because automation is exactly what I specialize in. I've built {script_count}+ automation scripts that have saved clients {hours_saved}+ hours of manual work.

**The Problem I Solve:**
{problem_description}

**My Solution:**
{solution_approach}""",
        
        "body": """
**Technical Approach:**

🔧 **Tools I'll Use:**
{tools_list}

📊 **Process:**
1. Analyze your current workflow ({analysis_duration})
2. Design optimized automation ({design_duration})
3. Build & test the solution ({build_duration})
4. Deploy with documentation ({deploy_duration})

**What Makes My Scripts Different:**
- Error handling for edge cases
- Detailed logging and monitoring
- Easy to modify and extend
- Comprehensive documentation
- Video walkthrough included

**Similar Projects:**
{portfolio_examples}

**Deliverables:**
{deliverables_list}
""",
        
        "closing": """
**Investment:** {price_range}

This includes everything: development, testing, documentation, and {support_duration} of support.

I'm ready to start immediately. Can we schedule a quick chat to discuss the specifics?

Looking forward to helping you reclaim your time!

Best,
{my_name}
{my_title}
"""
    },
    
    "data_analysis": {
        "opening": """Hi {client_name},

I saw your posting for {job_title} and wanted to reach out immediately. With {experience_years}+ years in data analysis and {project_count}+ projects completed, I specialize in turning raw data into actionable insights.

**Your Challenge:**
{problem_description}

**My Expertise:**
I don't just crunch numbers - I tell stories with data that drive business decisions.""",
        
        "body": """
**My Analysis Process:**

📥 **Data Collection & Cleaning**
   - Source verification and validation
   - Missing data handling
   - Outlier detection and treatment

📊 **Exploratory Analysis**
   - Statistical profiling
   - Pattern identification
   - Correlation analysis

📈 **Visualization & Reporting**
   - Executive dashboards
   - Detailed technical reports
   - Interactive charts and graphs

💡 **Insights & Recommendations**
   - Key findings summary
   - Actionable recommendations
   - Implementation roadmap

**Tools & Technologies:**
{tech_stack}

**Sample Deliverables:**
{deliverables_list}

**Previous Work:**
{portfolio_examples}
""",
        
        "closing": """
**Timeline:** {timeline}
**Investment:** {price_range}

I can start immediately and deliver initial insights within {first_deliverable_time}.

Would you like to schedule a brief call to discuss your data and goals?

Best regards,
{my_name}
{my_title}

{portfolio_url}
"""
    },
    
    "api_development": {
        "opening": """Hi {client_name},

I'm reaching out about your {job_title} project. API development is my core expertise - I've designed and built {api_count}+ APIs serving {request_count}+ million requests.

**Why APIs Matter:**
{api_value_prop}

**My Approach:**
I build APIs that are fast, secure, and developer-friendly from day one.""",
        
        "body": """
**Technical Architecture:**

⚡ **Performance**
   - Response time < {response_time}ms
   - Rate limiting and caching
   - Horizontal scaling ready

🔒 **Security**
   - Authentication & authorization
   - Input validation & sanitization
   - HTTPS/TLS enforcement

📚 **Documentation**
   - OpenAPI/Swagger specs
   - Interactive documentation
   - Code examples in multiple languages

🧪 **Testing**
   - Unit tests ({test_coverage}% coverage)
   - Integration tests
   - Load testing benchmarks

**Tech Stack Options:**
{tech_stack}

**API Features:**
{api_features}

**Similar Projects:**
{portfolio_examples}
""",
        
        "closing": """
**Development Timeline:** {timeline}
**Fixed Price:** {price_range} (includes everything)

I'll deliver:
✓ Fully functional API
✓ Complete documentation
✓ Deployment guide
✓ {support_duration} support

Ready to discuss your requirements. Available for a call this week?

Best,
{my_name}
{my_title}

{portfolio_url}
"""
    },
    
    "general": {
        "opening": """Hi {client_name},

I hope you're doing well. I came across your project for {job_title} and I'm excited about the opportunity to help.

**Why Me:**
{unique_selling_point}

**Understanding Your Needs:**
{problem_understanding}""",
        
        "body": """
**My Approach:**

🎯 **Phase 1: Understanding**
   - Detailed requirements gathering
   - Clarifying questions
   - Scope definition

⚙️ **Phase 2: Execution**
   - Regular progress updates
   - Quality checkpoints
   - Collaborative feedback loops

✅ **Phase 3: Delivery**
   - Final review and testing
   - Documentation and handover
   - Post-project support

**Relevant Experience:**
{portfolio_examples}

**What You'll Receive:**
{deliverables_list}
""",
        
        "closing": """
**Timeline:** {timeline}
**Investment:** {price_range}

I'm ready to start {start_timeline} and committed to delivering exceptional results.

Would you be available for a quick call to discuss the details? I'd love to learn more about your project.

Best regards,
{my_name}
{my_title}

{portfolio_url}
"""
    }
}

# Default values for placeholders
DEFAULTS = {
    "my_name": "Your Name",
    "my_title": "Full-Stack Developer & Automation Expert",
    "experience_years": "5",
    "client_count": "50",
    "script_count": "100",
    "api_count": "25",
    "project_count": "75",
    "hours_saved": "1000",
    "request_count": "10",
    "response_time": "100",
    "test_coverage": "90",
    "portfolio_url": "your