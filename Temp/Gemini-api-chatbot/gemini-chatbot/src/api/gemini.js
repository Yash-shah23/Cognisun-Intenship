// src/api/gemini.js
import { GoogleGenerativeAI } from '@google/generative-ai';

// Retrieve API key from environment variables
const API_KEY = process.env.REACT_APP_GEMINI_API_KEY;

// --- API Key Validation ---
if (!API_KEY) {
  console.error(
    'ERROR: Gemini API Key not found. ' +
    'Please ensure REACT_APP_GEMINI_API_KEY is set in your .env file ' +
    'and that your React app has been restarted after setting it.'
  );
  // In a real application, you might throw an error or disable functionality here
  // For now, we'll let it proceed but expect API calls to fail.
}

// Initialize the Generative AI client
const genAI = new GoogleGenerativeAI(API_KEY);

// --- Model Configuration ---
// Choose a model that suits your needs.
// 'gemini-pro' is ideal for text-only conversations.
// 'gemini-pro-vision' is for multimodal inputs (text + images).
const TEXT_ONLY_MODEL = 'gemini-1.5-flash'; // Or 'gemini-1.5-pro' for more advanced tasks
// const MULTIMODAL_MODEL = 'gemini-pro-vision'; // Uncomment if you plan to use images

const textModel = genAI.getGenerativeModel({ model: TEXT_ONLY_MODEL });
// const multimodalModel = genAI.getGenerativeModel({ model: MULTIMODAL_MODEL }); // Uncomment for multimodal

/**
 * Sends a single prompt to the Gemini API and returns the text response.
 * This is suitable for single-turn questions or stateless interactions.
 *
 * @param {string} prompt The user's input prompt.
 * @returns {Promise<string>} The AI's response text.
 */
export const getGeminiResponse = async (prompt) => {
  if (!API_KEY) {
    return 'Error: Gemini API Key is missing. Please check your setup.';
  }

  try {
    const result = await textModel.generateContent(prompt);
    const response = await result.response;
    const text = response.text();
    return text;
  } catch (error) {
    console.error('Error getting response from Gemini (single-turn):', error);
    // Return a more informative error message to the user
    return `Sorry, something went wrong. Error: ${error.message || 'Unknown error'}. Please try again.`;
  }
};

// --- Multi-Turn Chat Functions (for maintaining conversation history) ---
// These functions are designed for a stateful chat session where the AI remembers previous turns.

/**
 * Initializes a new chat session with the Gemini model.
 * Call this when a user starts a new conversation.
 *
 * @returns {import('@google/generative-ai').ChatSession} A new chat session object.
 */
export const startNewChatSession = () => {
  if (!API_KEY) {
    console.error('Cannot start new chat session: Gemini API Key is missing.');
    return null; // Or throw an error
  }
  // history can be pre-populated if you want to give the AI context from the start
  const chat = textModel.startChat({ history: [] });
  console.log('New Gemini chat session started.');
  return chat;
};

/**
 * Sends a message within an ongoing chat session and returns the AI's response.
 * The session automatically manages the conversation history.
 *
 * @param {import('@google/generative-ai').ChatSession} chat The active chat session object.
 * @param {string} message The user's message.
 * @returns {Promise<string>} The AI's response text.
 */
export const sendMessageToGeminiChat = async (chat, message) => {
  if (!chat) {
    console.error('Attempted to send message to a null chat session.');
    return 'Error: Chat session not initialized.';
  }
  if (!API_KEY) {
    return 'Error: Gemini API Key is missing. Cannot send message.';
  }

  try {
    const result = await chat.sendMessage(message);
    const response = await result.response;
    const text = response.text();
    return text;
  } catch (error) {
    console.error('Error sending message to Gemini chat session:', error);
    // Return a more informative error message to the user
    return `Sorry, something went wrong with the conversation. Error: ${error.message || 'Unknown error'}. Please try again.`;
  }
};

// --- Example for Multimodal Input (if you plan to add image upload) ---
/*
// Helper function to convert a File object to a GoogleGenerativeAI.Part
async function fileToGenerativePart(file) {
  const base64EncodedDataPromise = new Promise((resolve) => {
    const reader = new FileReader();
    reader.onloadend = () => resolve(reader.result.split(',')[1]);
    reader.readAsDataURL(file);
  });
  return {
    inlineData: {
      data: await base64EncodedDataPromise,
      mimeType: file.type,
    },
  };
}

// Function to send text and image to a multimodal model
export const getGeminiVisionResponse = async (textPrompt, imageFile) => {
  if (!multimodalModel) {
    console.error('Multimodal model not initialized.');
    return 'Error: Multimodal capabilities not available.';
  }
  if (!API_KEY) {
    return 'Error: Gemini API Key is missing. Cannot send multimodal request.';
  }

  try {
    const imagePart = await fileToGenerativePart(imageFile);
    const result = await multimodalModel.generateContent([textPrompt, imagePart]);
    const response = await result.response;
    const text = response.text();
    return text;
  } catch (error) {
    console.error('Error getting response from Gemini Vision:', error);
    return `Sorry, something went wrong with image processing. Error: ${error.message || 'Unknown error'}. Please try again.`;
  }
};
*/