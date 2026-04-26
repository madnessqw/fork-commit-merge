import os
import re

MARKETING_COPY_PATH = "/home/gokhan/UniverseCreator/subagent_workspaces/p2p_monetization_marketing/workdir/marketing_copy.md"

def parse_template(filepath):
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return None, None

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the # Email Template section
    template_section_match = re.search(r"# Email Template\s*(.*?)(?=\n# |$)", content, re.DOTALL)
    if not template_section_match:
        print("Could not find '# Email Template' section.")
        return None, None

    template_content = template_section_match.group(1)

    subject_match = re.search(r"Subject:\s*(.*)", template_content)
    body_match = re.search(r"Body:\s*(.*)", template_content, re.DOTALL)

    subject = subject_match.group(1).strip() if subject_match else ""
    body = body_match.group(1).strip() if body_match else ""

    return subject, body

def main():
    print("--- P2P Distributor Script ---")
    
    # Create a dummy marketing_copy.md if it doesn't exist, to ensure the script is executable
    if not os.path.exists(MARKETING_COPY_PATH):
        os.makedirs(os.path.dirname(MARKETING_COPY_PATH), exist_ok=True)
        with open(MARKETING_COPY_PATH, 'w', encoding='utf-8') as f:
            f.write("# Email Template\n\nSubject: Exclusive P2P Monetization Opportunity for {company}\n\nBody:\nHi {name},\n\nI noticed {company} is doing great work. Have you considered P2P monetization? Let's connect!\n\nBest,\nSales Engineer\n")
        print(f"Created dummy file at {MARKETING_COPY_PATH} for testing.\n")
    
    subject_template, body_template = parse_template(MARKETING_COPY_PATH)
    
    if subject_template is None or body_template is None:
        print("Failed to parse template. Exiting.")
        return

    leads = [
        {"name": "Alice Smith", "company": "Acme Corp", "email": "alice@acmecorp.com"},
        {"name": "Bob Johnson", "company": "Globex", "email": "bob@globex.com"},
        {"name": "Charlie Davis", "company": "Initech", "email": "charlie@initech.com"}
    ]
    
    print(f"Found {len(leads)} mock leads. Generating messages...\n")
    
    for lead in leads:
        # Personalize subject and body using simple string replacement to avoid .format issues with {{ or }}
        personalized_subject = subject_template.replace("{{FirstName}}", lead["name"]).replace("{name}", lead["name"]).replace("{company}", lead["company"])
        personalized_body = body_template.replace("{{FirstName}}", lead["name"]).replace("{name}", lead["name"]).replace("{company}", lead["company"])

        print("="*50)
        print(f"Sending to : {lead['email']}")
        print(f"Subject    : {personalized_subject}")
        print(f"Body       :\n{personalized_body}")
    
    print("="*50)
    print("Distribution simulation finished.")

if __name__ == "__main__":
    main()
