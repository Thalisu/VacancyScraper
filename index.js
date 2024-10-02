const { exec } = require("node:child_process");

class JobScrapper {
  venvActivate = ". venv/bin/activate";
  linkedinPath = "python3 src/linkedin.py";
  args = "";

  constructor(keywords, location, timeframe, remote, page) {
    this.args = `'${keywords}' '${location}' '${timeframe}' '${remote}' '${page}'`;
    console.log(this.args);
  }

  linkedin() {
    const jobs = new Promise((resolve, reject) => {
      exec(
        `${this.venvActivate} && ${this.linkedinPath} ${this.args}`,
        (err, stdout, stderr) => {
          if (err) {
            reject(err);
          }
          resolve(stdout);
        }
      );
    });
    return JSON.parse(jobs);
  }
}

module.exports = JobScrapper;
