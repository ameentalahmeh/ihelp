# iHelp  

AI assistant that adapts to any business, automating tasks and providing seamless customer support.  

## Overview  

iHelp is a fast and intuitive platform designed to help businesses create AI-powered customer support assistants with ease.  

Built on **IBM Watson AI technology** and **TogetherAI**, iHelp enables businesses to:  

- Automate customer support.  
- Provide real-time assistance.  
- Deliver accurate answers to common queries—all without the need for coding.  

### **Key Benefit**  
Launch an AI assistant for your business in minutes—no coding required.  


## **Key Features**  

1. **No Coding Required**  
   - Set up your assistant in minutes with an intuitive user interface.  

2. **Automatic Content Summarization**  
   - iHelp scans and summarizes your website content to provide a knowledge base for your assistant.  

3. **IBM Watson AI Integration**  
   - Leverages IBM Watson’s conversational AI to handle customer interactions effectively.  

4. **TogetherAI Enhanced Functionality**  
   - Improves conversational flows and language understanding.  

5. **24/7 Customer Support**  
   - Enable your assistant to provide continuous support anytime, anywhere.  

6. **Easy Management**  
   - Manage and update your assistant’s intents, actions, and responses effortlessly.  


## **Future Work**  

1. **Expand Knowledge Base**  
   - Enable integrations with external data sources for a richer knowledge repository.  

2. **Multilingual Support**  
   - Allow businesses to create assistants that support multiple languages.  

3. **Enhanced Personalization**  
   - Tailor responses to specific customer profiles.  

4. **UI Improvements**  
   - Enhance the interface to provide even more streamlined workflows.  


## **Tools & Technologies Used**  

- **Streamlit**: For building the user interface.  
- **IBM Watson Assistant**: To power conversational AI capabilities.  
- **TogetherAI**: For enhanced conversational and natural language understanding.  
- **Llama Index**: For efficient content summarization and question-answer generation.  
- **LLMs**: For language understanding and automation.  


## **How iHelp Works**  

### **Step 1: Enter Your Website URL**  
iHelp scans your website and extracts important information, such as FAQs, product details, and contact information.  

### **Step 2: Automatic Summarization**  
Using AI, iHelp generates a concise summary of the extracted content.  

### **Step 3: Create Watson Assistant Workspace**  
iHelp uses IBM Watson AI, TogetherAI, and Llama 3.2 to generate:  

- **Workspace Details**: Name, description, version, and more.  
- **Intents**: Questions users might ask.  
- **Actions/Dialog Nodes**: Responses to queries.  
- Outputs all data in **JSON format**.  

### **Step 4: Download and Deploy**  
- Export your generated Watson Assistant Workspace as a `.json` file.  
- Import it into IBM Watson Assistant, link your assistant, and you're ready to go!  


## **Getting Started**  

### **Step 1: Set Up a Virtual Environment**  

1. Create a virtual environment:  
   ```bash
   python -m venv .venv
   ```  

2. Activate the virtual environment:  
   - On Windows:  
     ```bash
     .venv\Scripts\activate
     ```  
   - On macOS/Linux:  
     ```bash
     source .venv/bin/activate
     ```  

3. Install the required libraries:  
   ```bash
   pip install streamlit ibm-watson ibm_cloud_sdk_core llama-index python-dotenv bs4 tldextract urllib3
   ```  


### **Step 2: Launch the App**  

1. Run the app:  
   ```bash
   streamlit run app.py
   ```  

2. Follow the steps to:  
   - Enter your website URL.  
   - Summarize the website content.  
   - Generate and download the Watson Assistant Workspace JSON.  


### **Step 3: Import the JSON File**  

1. Log in to IBM Watson Assistant.  
2. Import the JSON file to create your assistant workspace.  
3. Configure deployment and test your assistant.  


## **Screenshots for Steps**  

### 1. **Homepage**  
User-friendly dashboard to guide you through creating your assistant.  

![Homepage](#)  


### 2. **Enter Website URL**  
Simple input box to scan your website for relevant content.  

![Enter URL](#)  


### 3. **Content Summarization**  
View and edit the summarized content extracted from your website.  

![Summarization](#)  


### 4. **Generate Workspace**  
Real-time creation of Watson Assistant Workspace JSON.  

![Generate Workspace](#)  


### 5. **Download Assistant JSON**  
Export your assistant configuration as a `.json` file.  

![Download JSON](#)
