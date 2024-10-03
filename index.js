import { exec } from "child_process";

class JobScrapper {
  venvActivate = ". ./VacancyScrapper/venv/bin/activate";
  linkedinPath = "python3 ./VacancyScrapper/src/linkedin.py";
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

export default JobScrapper;
