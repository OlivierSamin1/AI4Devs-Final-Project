import logging
import requests
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

logger = logging.getLogger(__name__)

@api_view(['GET'])
def health_check(request):
    """Health check endpoint for the API"""
    return Response({'status': 'healthy', 'service': 'api'})

@api_view(['POST'])
def chat(request):
    """Handle chat messages and return responses"""
    try:
        message = request.data.get('message', '')
        if not message:
            return Response({'error': 'No message provided'}, status=400)
        
        logger.info(f"Received chat message: {message}")
        
        # Process the message
        response_text = process_chat_message(message)
        
        return Response({'message': response_text})
    except Exception as e:
        logger.error(f"Error processing chat message: {str(e)}")
        return Response({'error': 'Internal server error'}, status=500)

def process_chat_message(message):
    """Process a chat message and return a response"""
    try:
        # Basic echo response for testing
        if 'hello' in message.lower():
            return "Hello! How can I help you with your health symptoms today?"
        
        # Try to query the API bridge for health data
        api_bridge_url = settings.API_BRIDGE_URL
        try:
            # Format a simple query to test if there's a symptom keyword
            symptom_keywords = ['headache', 'pain', 'fever', 'cough', 'cold', 'flu', 'symptom']
            query_needed = any(keyword in message.lower() for keyword in symptom_keywords)
            
            if query_needed:
                # Send request to API bridge
                response = requests.post(
                    f"{api_bridge_url}/query",
                    json={'query': f"SELECT * FROM health_symptoms WHERE description LIKE '%{message}%' LIMIT 5"},
                    timeout=5
                )
                
                if response.status_code == 200:
                    data = response.json().get('result', [])
                    if data:
                        results = "\n".join([f"- {item.get('description', 'Unknown symptom')}" for item in data])
                        return f"I found these matches for '{message}':\n{results}"
                    else:
                        return f"I couldn't find any health records matching '{message}'. Please try a different query."
            
            # Default response if no API bridge query was made or needed
            return f"I received your message about '{message}'. How else can I help you with your health data?"
            
        except requests.RequestException as e:
            logger.error(f"Error connecting to API bridge: {str(e)}")
            return "I'm having trouble connecting to the database right now. Please try again later."
    
    except Exception as e:
        logger.error(f"Error in process_chat_message: {str(e)}")
        return "I'm sorry, I couldn't process your request. Please try again." 