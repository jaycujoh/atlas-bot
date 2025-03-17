from openai import OpenAI
import logging
from config.settings import OPENAI_API_KEY

# Initialize OpenAI client
openai_client = OpenAI(api_key=OPENAI_API_KEY)

def generate_analysis_with_openai(player_data, replay, player_name, max_retries=3):
    """Generates an analysis of the replay using OpenAI's GPT-4."""
    retries = 0
    while retries < max_retries:
        try:
            player = next(player for player in replay.players if player.name == player_name)
            opponent = next(player for player in replay.players if player.name != player_name)

            # Create a detailed prompt for the AI
            prompt = (
                f"ATLAS AI ANALYSIS MODE ACTIVATED. ANALYZING REPLAY DATA FOR {player_name} ({player.play_race}) "
                f"VERSUS {opponent.name} ({opponent.play_race}).\n\n"
                f"DIRECTIVE: PROVIDE TACTICAL ANALYSIS IN A ROBOTIC, SCI-FI TONE. "
                f"ANALYSIS MUST FOLLOW THIS EXACT FORMAT. DEVIATION IS NOT ACCEPTABLE.\n\n"
                f"FORMAT:\n"
                f">>> ANALYSIS INITIATED...\n"
                f">>> PROCESSING DATA STREAM... COMPLETE.\n"
                f">>> COMMENCING REPORT GENERATION...\n\n"
                f"⚠️ STRATEGIC SUCCESS: [DETAILS].\n\n"
                f"⚠️ TACTICAL WEAKNESS: [DETAILS].\n\n"
                f"⚠️ COUNTER-STRATEGY: [DETAILS].\n\n"
                f"⚠️ RECOMMENDATION: [DETAILS].\n\n"
                f">>> ANALYSIS COMPLETE. END OF REPORT.\n\n"
                f"ADDITIONAL INSTRUCTIONS:\n"
                f"1. Ensure the analysis is based on the following replay data:\n"
                f"   - Units Produced: {player_data[player_name]['units_produced']}\n"
                f"   - Build Order: {player_data[player_name]['build_order']}\n"
                f"2. Provide specific, actionable advice for {player_name} to improve.\n"
                f"3. Do not include a RESOURCES section. Focus on providing more details in the existing sections.\n"
                f"4. Do not deviate from the provided format. Any deviation will result in an error.\n"
                f"5. Keep the subject headers (e.g., STRATEGIC SUCCESS, TACTICAL WEAKNESS) in CAPITAL LETTERS.\n"
                f"6. The details of each subject must remain in normal sentence case.\n"
                f"7. Do not add extra sections, comments, or explanations outside the provided format.\n"
                f"8. Do not use bullet points or numbered lists outside the RESOURCES section.\n"
                f"9. Do not include any additional text before or after the report.\n"
                f"10. Ensure there is a BLANK LINE between each section (e.g., between STRATEGIC SUCCESS and TACTICAL WEAKNESS).\n"
                f"11. If you cannot generate a response that fits the format, return 'ERROR: ANALYSIS FAILED. REBOOTING ATLAS AI...'"
            )

            # Generate a response using OpenAI's GPT-4
            response = openai_client.chat.completions.create(
                model="gpt-4",  # Use GPT-4
                messages=[
                    {"role": "system", "content": "You are ATLAS AI, a Terran tactical analysis system. Respond in a robotic, sci-fi tone."},
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1000,  # Increased from 600 to allow for more detailed analysis
                temperature=0.7,
            )

            # Extract the generated text
            analysis = response.choices[0].message.content.strip()

            # Check if the response contains the error message
            if "ERROR: ANALYSIS FAILED. REBOOTING ATLAS AI..." in analysis:
                logging.warning(f"Analysis failed. Retrying... (Attempt {retries + 1}/{max_retries})")
                retries += 1
                continue  # Retry the analysis

            # Format the response in a code block
            formatted_response = f"```\n{analysis}\n```"
            return formatted_response

        except Exception as e:
            logging.error(f"Error generating analysis with OpenAI: {e}")
            retries += 1
            if retries >= max_retries:
                return "```\n>>> ERROR: ANALYSIS FAILED. REBOOTING ATLAS AI...\n```"

    # If all retries fail, return an error message
    return "```\n>>> ERROR: ANALYSIS FAILED. REBOOTING ATLAS AI...\n```"