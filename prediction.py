import os
import cohere
from cohere.classify import Example
from dotenv import load_dotenv


class CohereService:
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.client = cohere.Client(os.getenv("COHERE_API_KEY"))

    def get_categories(self, feedback: str) -> str:
        response = self.client.classify(inputs=[feedback], examples=examples)
        return response.classifications[0].prediction


examples = [
    Example("This app is pretty slow and unresponsive.", "Speed"),
    Example("The website didn't load on time.", "Speed"),
    Example("The application was not fast enough for my needs.", "Speed"),
    Example("I didn't like the app because it was too slow.", "Speed"),
    Example("Your application is very slow, which made me not want to use it.", "Speed"),
    Example("Your application looks bad.", "Design"),
    Example("I didn't like the colour scheme of your application.", "Design"),
    Example("The colours of your app look bad.", "Design"),
    Example("Your application is ugly.", "Design"),
    Example("I wish your application looked better.", "Design"),
    Example("I don't like the look of your website.", "Design"),
    Example(
        "Your application does not have keyboard navigation, so it is not accessible for people with limited mobility.",
        "Accessibility"
    ),
    Example("I couldn't navigate your website with keyboard, which means it wasn't accessible.", "Accessibility"),
    Example(
        "Your app is not accessible for those with limited mobility, because it does not have keyboard navigation.",
        "Accessibility"
    ),
    Example(
        "Your images do not have alt text, making it less accessible to people with a screen reader.",
        "Accessibility"
    ),
    Example(
        "The images in the app don't have alt text, so it isn't accessible for the visually impaired.",
        "Accessibility"
    ),
    Example("The app has low colour contrast, so it's not accessible to the visually impaired.", "Accessibility"),
    Example("Your website has low colour contrast, so it's not accessible to people with low vision.", "Accessibility"),
    Example(
        "The application has low colour contrast, which means it's less accessible for the blind.",
        "Accessibility"
    ),
    Example("It was hard to learn the features of your website.", "Usability"),
    Example("The application has a big learning curve.", "Usability"),
    Example("Your app is hard to learn.", "Usability"),
    Example("The app has too many features.", "Usability"),
    Example("Your application is difficult to use.", "Usability"),
    Example("Your website is hard to learn.", "Usability"),
    Example("I'm finding it hard to use the application.", "Usability"),
    Example("The app is hard to use.", "Usability"),
    Example("I can't tell how to use your app.", "Usability")
]
