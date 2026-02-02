Here’s a self-contained GitHub Actions workflow you can drop into `.github/workflows/pr-validate.yml` to enforce your two rules. It will:

1. Detect which `accounts/<name>/` directory is touched and fail if more than one is modified
    
2. Label the PR with `account:<name>` (removing any old `account:*` labels), so you can see at a glance which root module it’s touching
    
3. Use the GitHub API to block the PR (fail the check) if _another_ open PR that’s labeled for the _same_ account currently has an in‐progress validation run
    

Finally, you’ll configure a branch‐protection rule that _requires_ this workflow to pass before merging.

```yaml
# .github/workflows/pr-validate.yml
name: "Validate Terraform Root Module PR"

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review]

jobs:
  validate:
    runs-on: ubuntu-latest
    # fail fast if someone tries to merge two modules in one PR
    steps:
      - name: Check out code
        uses: actions/checkout@v3
        with:
          fetch-depth: 0

      - name: Determine changed 'accounts/' modules
        id: changed
        run: |
          # get all files changed against the base branch
          git fetch origin ${{ github.base_ref }} --depth=1
          CHANGED=$(git diff --name-only origin/${{ github.base_ref }} ${{ github.sha }})
          echo "Changed files:"
          echo "$CHANGED"

          # extract unique account names (accounts/<name>/...)
          MODULES=$(echo "$CHANGED" \
            | grep -E '^accounts/[^/]+/' \
            | cut -d/ -f2 \
            | sort -u \
            | tr '\n' ' ')
          COUNT=$(echo "$MODULES" | wc -w)
          echo "::set-output name=modules::$MODULES"
          echo "::set-output name=count::$COUNT"

      - name: Enforce single-module rule
        if: steps.changed.outputs.count != '1'
        run: |
          echo "❌ This PR modifies ${steps.changed.outputs.count} accounts/* directories:"
          echo "   ${steps.changed.outputs.modules}"
          echo "Please modify exactly one 'accounts/<name>' per PR."
          exit 1

      - name: Export ACCOUNT
        run: echo "ACCOUNT=${{ steps.changed.outputs.modules }}" >> $GITHUB_ENV

      - name: Remove old account:* labels
        uses: actions-ecosystem/action-remove-labels@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          labels: |
            account:*

      - name: Add account label
        uses: actions-ecosystem/action-add-labels@v1
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          labels: |
            account:${{ env.ACCOUNT }}

      - name: Prevent concurrent validations on same account
        uses: actions/github-script@v6
        with:
          github-token: ${{ secrets.GITHUB_TOKEN }}
          script: |
            const accountLabel = `account:${process.env.ACCOUNT}`;
            // list all open PRs with this label
            const issues = await github.paginate(
              github.rest.issues.listForRepo,
              {
                owner: context.repo.owner,
                repo:  context.repo.repo,
                labels: accountLabel,
                state:  "open",
              }
            );
            // filter to PRs other than this one
            const others = issues.filter(i => i.pull_request && i.number !== context.issue.number);

            if (others.length) {
              // for each other PR, see if a validation run is in_progress
              const runs = await github.paginate(
                github.rest.actions.listWorkflowRunsForRepo,
                {
                  owner:       context.repo.owner,
                  repo:        context.repo.repo,
                  status:      "in_progress",
                  per_page:    100,
                }
              );
              for (const pr of others) {
                for (const run of runs) {
                  if (
                    run.event === "pull_request" &&
                    run.pull_requests.some(p => p.number === pr.number)
                  ) {
                    core.setFailed(
                      `❌ Another PR (#${pr.number}) for '${process.env.ACCOUNT}' ` +
                      `is still running validation. Please wait for it to finish.`
                    );
                  }
                }
              }
            }

```
### How to hook this up in GitHub

1. **Commit** the above to `.github/workflows/pr-validate.yml`.
    
2. In **Settings → Branches** add (or edit) your branch‐protection rule on `main` (or your protected branch) to **require status checks** and select the “Validate Terraform Root Module PR” check.
    
3. Now:
    
    - If you touch more than one `accounts/` subdir, the check will ☓ fail immediately.
        
    - If someone else already has a PR against `accounts/a` whose validation is still running, your PR against `accounts/a` will likewise ☓ fail until that one completes.
        
    - PRs against different accounts (e.g. one for `accounts/a`, another for `accounts/b`) run in parallel and can both pass → both can merge.
        

---

### References

- **actions/checkout**: [https://github.com/actions/checkout](https://github.com/actions/checkout)
    
- **action-add-labels**: [https://github.com/actions-ecosystem/action-add-labels](https://github.com/actions-ecosystem/action-add-labels)
    
- **action-remove-labels**: [https://github.com/actions-ecosystem/action-remove-labels](https://github.com/actions-ecosystem/action-remove-labels)
    
- **actions/github-script**: [https://github.com/actions/github-script](https://github.com/actions/github-script)
    
- **Branch protection** (require status checks):  
    [https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-protected-branches/about-protected-branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-protected-branches/about-protected-branches)