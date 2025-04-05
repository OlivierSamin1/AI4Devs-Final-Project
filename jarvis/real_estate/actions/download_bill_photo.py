import os.path
import subprocess
from django.contrib import messages


class Photo:

    directories = []
    success_messages = []
    error_message = ["The photos are in several folders:"]

    def handle(self, request, queryset):
        self.success_messages = ["The photos are in the opened window and have the following names:"]
        for item in queryset.all():
            self.directories.append(os.path.dirname(item.photo.path))
            self.success_messages.append(os.path.basename(item.photo.path))
        self.directories = list(set(self.directories))
        print(self.directories)
        if len(self.directories) == 1:
            self.directories = self.directories[0]
            subprocess.Popen(['xdg-open', self.directories])
            for message in self.success_messages:
                messages.add_message(request, messages.INFO, message)
        else:
            for directory in self.directories:
                messages.add_message(request, messages.ERROR, directory)
