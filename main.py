from PyInquirer import style_from_dict, Token, prompt
import scraper
from os import listdir
import train

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


def chat_prompt():
    chat_menu = [{
        'type': 'list',
        'message': 'Select a chatbot',
        'name': 'chatbot',
        'choices': ['< Back']  # must be filled at runtime
    }]

    chatbot = prompt(chat_menu, style=style)['chatbot']


def train_prompt():
    train_menu = [{
        'type': 'list',
        'message': 'Select a dataset',
        'name': 'dataset',
        'choices': ['< Back'] + [str(f) for f in listdir('./data')]
    }]

    dataset = prompt(train_menu, style=style)['dataset']

    if dataset == '< Back':
        pass
    else:
        train.train()


def dl_prompt():
    dl_menu = [{
        'type': 'list',
        'message': 'Select a source',
        'name': 'source',
        'choices': [{
            'key': 'r',
            'name': 'Reddit',
            'value': 'reddit',
        }, {
            'key': 't',
            'name': 'Twitter',
            'value': 'twitter',
        }]
    }, {
        'type': 'input',
        'message': 'Enter the user\'s name to download his public messages.',
        'name': 'user',
    }, {
        'type': 'confirm',
        'message': 'Include comments and replies ?',
        'name': 'include_all',
    }]

    answers = prompt(dl_menu, style=style)

    if answers['source'] == 'reddit':
        scraper.scrape_reddit(answers['user'], not answers['include_all'])
    elif answers['source'] == 'twitter':
        scraper.scrape_twitter(answers['user'], not answers['include_all'])


while True:
    main_menu = [{
        'type': 'list',
        'message': 'Select an action',
        'name': 'action',
        'choices': [{
            'key': 'k',
            'name': 'Chat',
            'value': 'chat',
        }, {
            'key': 'd',
            'name': 'Download new training data',
            'value': 'dl',
        }, {
            'key': 't',
            'name': 'Train a new chatbot',
            'value': 'train',
        }]
    }]

    action = prompt(main_menu, style=style)['action']

    if action == 'chat':
        chat_prompt()
    elif action == 'dl':
        dl_prompt()
    elif action == 'train':
        train_prompt()
