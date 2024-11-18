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
   - Using AI, iHelp scans and summarizes your website content to provide a knowledge base for your assistant.

3. **IBM Watson AI Integration**
   - Leverages IBM Watson’s conversational AI to handle customer interactions effectively.

4. **24/7 Customer Support**
   - Enable your assistant to provide continuous support anytime, anywhere.

5. **Easy Management**
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
- **TogetherAI, Llama Index, and LLMs**: A powerful combination for enhanced language understanding and efficient content summarization.

## **How iHelp Works**

### **Step 1: Enter Your Website URL**
iHelp extracts important information from your website, such as FAQs, product details, and contact information.

### **Step 2: Automatic Summarization**
Using AI, iHelp generates a concise summary of the extracted content.

### **Step 3: Create IBM Watson Assistant Workspace**
iHelp uses IBM Watson AI, TogetherAI, and Llama 3.2 to generate:

- **Workspace Details**: Name, description, version, and more.
- **Intents**: Questions users might ask.
- **Actions/Dialog Nodes**: Responses to queries.
- Outputs all data in **JSON format**.

### **Step 4: Download and Update**
Export your workspace as a `JSON` file, update it, and redeploy it to your assistant—you're all set!

## **Getting Started**

### **Step 1: Set Up a Virtual Environment**

1. Clone the repo
   ```bash
   git clone git@github.com:ameentalahmeh/ihelp.git
   ```

2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

4. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

### **Step 2: Launch the App**

1. Run the app:
   ```bash
   streamlit run app.py
   ```

### **Step 3: Create Your Workspace**
   - Enter your website URL.
   - Wait for iHelp to summarize the website content and generate the Watson Assistant Workspace JSON.
   - If needed, export your Watson Assistant Workspace as a `.json` file to update it.

### **Step 4: Test Your AI Assistant**

   1. Log in to IBM Cloud Console.
   2. Link your Workspace with your Assistant in IBM Cloud.
   3. Import the JSON file to update your assistant conversations.
   4. Launch it, and make some inquiries.

## **Screenshots**

### 1. **Homepage**
User-friendly dashboard to guide you through creating your assistant.

![Homepage](/screenshots/home-view.jpeg)

### 2. **Enter Website URL**
Simple input box to scan your website for relevant content.

![fetching-and-summarizing](/screenshots/fetching-and-summarizing.jpeg)

### 3. **Content Summarization**
View and edit the summarized content extracted from your website.

![Summarization](/screenshots/content-document.jpeg)

### 4. **Generate Workspace**
Real-time creation of Watson Assistant Workspace JSON.

![Generate Workspace](/screenshots/workspace-create.jpeg)

### 5. **Download Workspace JSON**
If needed, export the generated Watson Assistant Workspace configuration as a `.json` file.

![Download JSON Workspace](/screenshots/workspace-json-complete.jpeg)

### 6. **View Sample Workspace JSON**
Preview a sample of the Watson Assistant Workspace JSON file to understand its structure.

![Sample Assistant JSON](/screenshots/workspace-json.jpeg)

### 7. **Test the Assistant**
Link the generated or updated Workspace JSON to your IBM Watson Assistant, and test your assistant in a real-world environment.

![Test Assistant](/screenshots/test-assistant-uses-workspace.jpeg)
