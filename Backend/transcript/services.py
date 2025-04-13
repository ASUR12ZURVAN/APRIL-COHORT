def analyze_call_transcript(transcript_text):
    """
    Processes raw call transcript text and structures it into labeled speaker turns.
    Returns: List of {'speaker': 'Agent'/'Customer', 'text': str} dictionaries
    """
    import re
    
    # Initialize variables
    structured_convo = []
    current_speaker = None
    sentences = re.split(r'(?<=[.!?])\s+', transcript_text.strip())
    
    for sentence in sentences:
        # Detect speaker changes
        if re.match(r'^(agent|customer|client|representative):', sentence.lower()):
            current_speaker = re.split(r'[:,\s]', sentence.lower())[0].capitalize()
            sentence = re.sub(r'^(agent|customer|client|representative):\s*', '', sentence, flags=re.I)
        elif not current_speaker:
            # Default first speaker to Agent if not specified
            current_speaker = 'Agent'
        
        # Clean and store the sentence
        if sentence:
            structured_convo.append({
                'speaker': current_speaker,
                'text': sentence
            })
            
            # Toggle speaker if no explicit labels
            if not re.match(r'^(agent|customer|client|representative):', sentence, flags=re.I):
                current_speaker = 'Customer' if current_speaker == 'Agent' else 'Agent'
    
    return structured_convo