SLACK_TOKEN = $(MASTERMIND_SLACK_TOKEN)
slack_org = mastermindmitm


# --secret LOGO_URL=$(logo_url)
wt-create:
	wt create https://raw.githubusercontent.com/auth0/webtask-slack-signup/master/slack-invite.js \
            --name $(slack_org)-signup \
            --capture \
            --secret SLACK_ORG=$(slack_org) \
            --secret SLACK_TOKEN=$(SLACK_TOKEN)
.PHONY: wt-create
