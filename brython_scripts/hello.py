from browser import document

for div in document.select('div'):
    div.attach('Hello!')
