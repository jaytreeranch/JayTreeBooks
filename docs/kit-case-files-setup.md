# JayTree Case Files — Kit Setup

Kit is the long-term newsletter backend for JayTree Case Files. Keep FormSubmit live until the Kit form is published and its embed code has been added to the website configuration.

## Recommended Kit account structure

- Plan: Newsletter
- Form name: `JayTree Case Files`
- Form type: Inline
- Fields: Email only
- Sequence: `JayTree Case Files Welcome`
- Confirmation: Double opt-in recommended
- Confirmation redirect: `https://www.JayTreeBooks.com/case-files-thanks.html`
- Sender name: `JayTree Books`
- Reply-to: `jaytreebooks@gmail.com`

## Create the form

1. In Kit, open **Audience growth → Landing Pages & Forms**.
2. Choose **+ New → Form → Inline**.
3. Name it `JayTree Case Files`.
4. Keep only the email field.
5. Use CTA copy such as `Open the Case Files`.
6. Set the confirmation email subject to `Confirm your JayTree Case Files access`.
7. Set the redirect to `https://www.JayTreeBooks.com/case-files-thanks.html`.
8. Save and publish.
9. Click **Embed → JavaScript** and copy the complete embed line.

## Connect the website

Save the Kit embed code in a local text file such as `kit_embed.txt`, then from the JayTreeBooks repository run:

```powershell
python scripts/configure_kit_newsletter.py --embed-file kit_embed.txt
```

Commit and push `config.js`. The website build workflow will run:

```text
build_reader_growth_site.py
finalize_reader_growth.py
apply_newsletter_provider.py
```

The final step replaces the FormSubmit forms only when `newsletter.provider` is `kit` and a valid Kit embed is present. Until then, FormSubmit stays live.

## Build the welcome sequence

Create one Kit Sequence named `JayTree Case Files Welcome` and use the copy in:

`data/case-files-welcome-sequence.md`

Suggested timing:

- Email 1: Immediately after confirmation
- Email 2: 2 days later
- Email 3: 3 days after Email 2

Add subscribers from the `JayTree Case Files` form to this sequence using Kit's automation tools.

## Import existing signups

Export or manually collect existing Case Files addresses captured through FormSubmit, then import them into Kit only if they previously gave marketing consent. Do not import unrelated Gmail contacts.

## Before switching traffic

Verify all of the following:

- Form appears on the homepage.
- Form appears on `/case-files.html`.
- Test signup receives the Kit confirmation email.
- Confirmation leads to the JayTree Books thank-you page.
- Subscriber enters the welcome sequence.
- Unsubscribe link is present in the delivered Kit email.
- GA4 still records `case_files_signup_submit` and `case_files_signup_complete`.
