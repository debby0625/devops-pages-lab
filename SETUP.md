# Setup and submission

## 1. Repository and identity

Use a repository with default branch `main`. A public repository supports Pages on GitHub Free and gives the grader read access. Confirm visibility before uploading course material.

Suggested repository: `debby0625/devops-pages-lab` (public). Created on 2026-10-29.

Upload the **contents** of this directory to the repository root, including `.github/workflows/`. README.md identifies 蔡逸盈 (debby0625). If you choose a different repository, update the absolute setup-guide link in README.md.

The activity workflow uses `github.repository_owner`; for an organization repository, replace that value with the individual student's username. The PAT must belong to that user.

## 2. Enable Pages

The basic site was first published from `main / (root)` with index.html. The advanced site replaces that entry with index.md and uses the custom build below. The basic page remains in Git history, avoiding competing homepage files.

In **Settings → Pages → Build and deployment → Source**, choose **GitHub Actions**. This implementation builds with Jekyll and deploys an artifact. The assignment's branch-source setting is an alternative implementation; do not combine it with this deployment workflow.

Open **Actions → Build and Deploy Pages → Run workflow** if needed. After success, open the URL shown by the `github-pages` deployment and capture the initial live page for A-level evidence.

Project URL: `https://USERNAME.github.io/REPOSITORY/`. A user repository named `USERNAME.github.io` uses `https://USERNAME.github.io/`.

## 3. Configure the required secret

Create a personal access token (classic) using the GitHub account whose activity is displayed. For this public course repository, use `public_repo` for public repository access; use `repo` only if private repository access is needed. Choose an expiration covering the grading period.

Store it under **Settings → Secrets and variables → Actions → New repository secret**, named exactly `TOKEN`. Enter it directly in GitHub; do not put the value in code, screenshots, reports or chat.

The PAT is supplied to the activity action. The specified action uses TOKEN for its GitHub API commit; the checkout uses the workflow repository token with `contents: read`. After the API commit, the workflow fetches main again so validation checks the committed README. A branch rule requiring PRs may block direct bot commits; check the rule and use an approved automation path if your repository enforces one.

`HIDE_DETAILS_ON_PRIVATE_REPOS` hides private activity details according to the action's behavior; prefer public activity for this public demonstration and inspect the generated content before submitting.

## 4. Generate activity and publish

1. Make a real public contribution, such as committing your initial site files.
2. Open **Actions → Update GitHub Activity → Run workflow** on `main`.
3. Verify the action-generated commit actually changes the activity section in README.md. A successful no-change run alone is not the required update evidence.
4. Wait for **Build and Deploy Pages** to complete after the activity run.
5. Open the live site and check that the activity items match README.md.

GitHub's event feed is eventually consistent. If no events are available, wait and rerun. A missing TOKEN or empty generated list fails the activity validation rather than claiming completion.

## 5. Evidence to retain

- Repository URL and Actions tab URL.
- Pages settings screenshot showing the chosen source.
- Initial live page screenshot and final live page screenshot showing activity. Record their URLs separately; screenshots need not include the address bar.
- Specific activity workflow run URL showing the update succeeded.
- Specific bot/action commit URL and diff showing the README activity change.
- Specific Pages workflow run URL and its source commit in the build summary.
- Verification that the grader can read the repository.

An activity run may finish without creating a new commit when the generated content is unchanged. Retain an earlier run that actually changed README.md, or make another real public contribution and rerun after the feed updates. If the action uses a token that triggers push workflows, both push and workflow_run may request a Pages build; concurrency serializes them.

## Validation and maintenance

Run `python3 scripts/validate_site.py` from this repository. CI also validates the actual Jekyll output before uploading it. Keep README markers intact, use `index.md` as the homepage, and avoid adding root `index.html` or `.nojekyll` to this Jekyll setup.

Do not remove branch protections solely to make automation pass. Expired/revoked secrets must be replaced in GitHub settings. Scheduled workflows run from the default branch and can be delayed; public repository schedules can be disabled after 60 days without activity.

## References

- [Specified activity Action and input reference](https://github.com/TheDanniCraft/activity-log)
- [GitHub Pages custom workflows](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [GitHub workflow triggers and repository-token behavior](https://docs.github.com/en/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow)
- [Scheduled workflows](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)


## Reproducible version and tests

The activity action is pinned to commit `130ff6ba97c30b2d272f27851db0a347b29472af` (v1 resolved on 2026-10-29). It commits through the GitHub API rather than updating the local checkout. `scripts/test_validation.py` runs normal source checks and isolated negative cases for missing/reversed markers, missing include, a competing index.html, and an empty activity feed. Temporary invalid copies are never deployed.
