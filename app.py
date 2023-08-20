#!/usr/bin/env python3
import aws_cdk as cdk

from stacks.bot_stack import BotStack


app = cdk.App()

BotStack(app, "BotStack")

cdk.Tags.of(app).add(key="owner", value="ali@datachef.co")
cdk.Tags.of(app).add(key="application", value="ConcertTelegramBot")

app.synth()
