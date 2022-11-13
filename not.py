from adaptivecards.adaptivecard import AdaptiveCard
from adaptivecards.elements import TextBlock
from adaptivecards.containers import Column, ColumnSet, Container

card = AdaptiveCard()
card.body = [
    Container(items=[
        TextBlock(text='Hello from adaptivecards', font_type='Default', size='Medium'),
        ColumnSet(columns=[
            Column(
                width='stretch',
                items=[
                    TextBlock(text='author', weight="Bolder", wrap=True),
                    TextBlock(text='version', weight="Bolder", wrap=True),
                ]
            ),
            Column(
                width='stretch',
                items=[
                    TextBlock(text='Huu Hoa NGUYEN', wrap=True),
                    TextBlock(text='0.1.0', wrap=True),
                ]
            )
        ])
    ]),
    TextBlock(text='more information can be found at [https://pypi.org/project/adaptivecards/](https://pypi.org/project/adaptivecards/)',
              wrap=True)
]
json_str = str(card)
print(json_str)