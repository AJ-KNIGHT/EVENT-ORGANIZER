import json
from django.core.management.base import BaseCommand
from eventapp.models import ChatbotQA

class Command(BaseCommand):
    help = 'Load chatbot questions, answers, and keywords from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('file', type=str, help='Path to the JSON file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                # Prepare a list of ChatbotQA objects
                chatbot_qa_list = [
                    ChatbotQA(
                        question=item['question'],
                        answer=item['answer'],
                        keywords=item['keywords']
                    )
                    for item in data
                ]
                # Use bulk_create to insert all records at once
                ChatbotQA.objects.bulk_create(chatbot_qa_list)
                self.stdout.write(self.style.SUCCESS('Successfully loaded data from JSON using bulk_create.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {e}'))