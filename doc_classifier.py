import os
from datetime import datetime
from langchain_openai import ChatOpenAI
from config import settings
from logger import logger

class DocClassifier:
    """
    Classifies a document with the initial 10 pages
    using llm
    """

    def __init__(self, document_text):
        self.class_labels = [
            "Finance", "Legal", "Operations", "HR", "Product", 
            "Engineering / Tech", "Sales", "Marketing / Communications", 
            "Customer Success / Support", "Strategy / Corp Dev", "Compliance / Risk", "Other"
        ]
        
        # Map each label to specific extraction prompts
        self.extraction_prompts = {
            "Finance": """
                Extract key financial information:
                - Document type (budget, forecast, invoice, audit report, financial statement)
                - Time period or fiscal year covered
                - Currency and monetary amounts (totals, line items, variances)
                - Budget categories or cost centers
                - Revenue, expenses, profit/loss figures
                - Key financial metrics or KPIs
                - Approval status and authorized personnel
                - Payment terms, due dates, or billing cycles
            """,
            
            "Legal": """
                Extract essential legal information:
                - Document type (contract, agreement, compliance doc, IP filing, regulation)
                - Parties involved (names, roles, entities)
                - Effective dates, terms, and expiration
                - Key obligations and rights
                - Financial terms and payment obligations
                - Governing law and jurisdiction
                - Compliance requirements or regulatory standards
                - Intellectual property details (patents, trademarks, copyrights)
                - Termination or renewal clauses
            """,
            
            "Operations": """
                Extract operational information:
                - Process or procedure name
                - Operational scope (facilities, logistics, supply chain)
                - Key steps, workflows, or procedures
                - Responsible teams or personnel
                - Performance metrics and KPIs
                - Resource requirements (equipment, materials, personnel)
                - Timeline and delivery schedules
                - Quality standards and compliance requirements
                - Vendor or supplier information
            """,
            
            "HR": """
                Extract human resources information:
                - Document type (policy, procedure, job description, benefits guide)
                - Employee information (roles, departments, levels)
                - Compensation details (salary ranges, benefits, equity)
                - Performance metrics and evaluation criteria
                - Training requirements and development programs
                - Compliance and regulatory requirements
                - Effective dates and review periods
                - Approval workflows and authorization levels
                - Employee relations policies and procedures
            """,
            
            "Product": """
                Extract product information:
                - Product name, version, or release information
                - Features, capabilities, and specifications
                - Target market and user personas
                - Development timeline and milestones
                - Technical requirements and dependencies
                - Research findings and user feedback
                - Design principles and UI/UX guidelines
                - Competitive analysis and market positioning
                - Success metrics and KPIs
                - Resource allocation and team assignments
            """,
            
            "Engineering / Tech": """
                Extract technical information:
                - System or application name
                - Technical architecture and infrastructure details
                - Code components, APIs, and integrations
                - Security requirements and protocols
                - Performance specifications and benchmarks
                - Development tools and frameworks
                - Deployment and configuration details
                - Monitoring and maintenance procedures
                - Version control and release information
                - Technical debt and improvement recommendations
            """,
            
            "Sales": """
                Extract sales information:
                - Customer or prospect information
                - Deal size, value, and probability
                - Sales stage and pipeline position
                - Product or service offerings
                - Pricing and discount structures
                - Key decision makers and stakeholders
                - Competitive landscape and positioning
                - Sales timeline and close dates
                - Terms and conditions
                - Follow-up actions and next steps
            """,
            
            "Marketing / Communications": """
                Extract marketing information:
                - Campaign name, type, and objectives
                - Target audience and market segments
                - Brand guidelines and messaging
                - Content type and distribution channels
                - Budget allocation and cost metrics
                - Performance metrics (CTR, conversion, ROI)
                - Timeline and key milestones
                - Creative assets and content requirements
                - Competitive analysis and market insights
                - PR strategy and media coverage details
            """,
            
            "Customer Success / Support": """
                Extract customer success information:
                - Customer name and account details
                - Support ticket or case information
                - Product usage and adoption metrics
                - Training materials and documentation
                - Onboarding processes and milestones
                - Customer feedback and satisfaction scores
                - Issue resolution steps and timelines
                - Escalation procedures and contacts
                - Success metrics and health scores
                - Renewal and expansion opportunities
            """,
            
            "Strategy / Corp Dev": """
                Extract strategic information:
                - Strategic initiative or project name
                - Business objectives and success metrics
                - Market analysis and competitive landscape
                - Partnership or M&A details (target, valuation, terms)
                - Investment information and funding rounds
                - OKRs (Objectives and Key Results)
                - Timeline and key milestones
                - Resource requirements and budget
                - Risk assessment and mitigation strategies
                - Stakeholder information and decision makers
            """,
            
            "Compliance / Risk": """
                Extract compliance and risk information:
                - Regulatory framework or standard (SOX, GDPR, HIPAA, etc.)
                - Compliance requirements and controls
                - Risk assessment findings and severity levels
                - Audit scope, methodology, and findings
                - Remediation actions and timelines
                - Responsible parties and oversight
                - Security measures and protocols
                - Incident details and response procedures
                - Certification status and renewal dates
                - Policy violations and corrective actions
            """,
            
            "Other": """
                Extract general document information:
                - Document type and purpose
                - Key topics or subjects covered
                - Important dates or deadlines
                - Main parties or entities mentioned
                - Critical information or decisions
                - Document source and context
                - Action items or next steps
                - Contact information if available
            """
        }
        
        self.document_text = document_text
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

    def classify_document(self) -> str:
        """
        Classify a document into one of the provided class labels using an LLM.
        
        Args:
            document_text (str): The text content of the document.
            
        Returns:
            str: The selected class label.
        """
        labels_str = ", ".join(self.class_labels)
        
        # Document classifier prompt
        prompt = f"""
            You are a document classifier. You are given a complete document below. 
            You must choose the most appropriate label from the following list that best suits the document:
            {labels_str}

            Document:
            \"\"\"{self.document_text}\"\"\"

            Make sure to choose only ONE label and provide ONLY the label as your answer.
        """

        logger.info(f"Before LLM call: {datetime.now()}")
        # Call the LLM and get the response.
        response = self.llm.invoke(prompt).content.strip()
        logger.info(f"After LLM call: {datetime.now()}")

        logger.info(f"Classification result: {response}")

        summary_prompt = f"""
        You are given a complete document below. Give me a summary that is no more than 1 line (255 characters).

        Document:
            \"\"\"{self.document_text}\"\"\"
        """

        raw_summary = self.llm.invoke(summary_prompt).content.strip()
        summary = raw_summary[:255]

        # Now do targeted extraction based on classification
        extracted_data = self.extract_by_type(response)
        
        return {
            "classification": response,
            "summary": summary,
            "extracted_data": extracted_data
        }

    def extract_by_type(self, document_type: str) -> dict:
        """
        Extract specific information based on document classification.
        This replaces the database prompt lookup system.
        """
        extraction_prompt = self.extraction_prompts.get(document_type, self.extraction_prompts["Other"])
        
        full_prompt = f"""
        Based on the document type "{document_type}", extract the following information:
        
        {extraction_prompt}
        
        Document Content:
        \"\"\"{self.document_text}\"\"\"
        
        Return the extracted information in a structured format. If any information is not found, indicate "Not specified".
        """
        
        logger.info(f"Extracting data for document type: {document_type}")
        extraction_response = self.llm.invoke(full_prompt).content.strip()
        
        return {
            "document_type": document_type,
            "extracted_info": extraction_response
        }