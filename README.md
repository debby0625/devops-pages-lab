# DevOps Activity Journal

Owner: 蔡逸盈 (debby0625)  
Course: DevOps

A static GitHub Pages site with an activity feed maintained by GitHub Actions.
The homepage includes this README, so the repository and website share one source of content.

[Live website](https://debby0625.github.io/devops-pages-lab/) · [Workflow runs](https://github.com/debby0625/devops-pages-lab/actions)

## Latest activity

<!--START_SECTION:activity-->
Activity has not been fetched yet. Run **Update GitHub Activity** after configuring the `TOKEN` secret.
<!--END_SECTION:activity-->

## How publishing works

1. A scheduled or manual workflow reads the repository owner's GitHub activity.
2. The activity action updates the marked section above and commits any changes.
3. The Pages workflow validates the source and builds `index.md` with Jekyll.
4. The validated HTML artifact is deployed to GitHub Pages.

## Schedule and enhancements

- Scheduled at **08:17, 14:17 and 20:17 Asia/Taipei** (00:17, 06:17 and 12:17 UTC).
- Three updates per day suit a course journal; manual runs support demonstrations.
- Running at minute 17 avoids scheduling directly at the start of an hour. GitHub scheduling can still be delayed.
- A responsive layout supports light and dark mode and keyboard navigation.
- Validation checks the activity markers, README include and rendered homepage before deployment.
- The Pages workflow also runs after a successful activity workflow, so publishing does not rely on a bot commit triggering another push workflow.

Activity comes from GitHub's events feed and may appear after a delay. This is not a complete contribution history.

## Setup

See [the setup guide](https://github.com/debby0625/devops-pages-lab/blob/main/SETUP.md) for repository settings, token configuration and evidence capture.

