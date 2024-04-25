document.addEventListener("alpine:init", () => {
    Alpine.data("jobFetcher", () => ({
      scrapingInProgress: false,
      jobs: [],
      selectedWebsite: '',

      init() {
        this.loadJobsFromStorage();
      },

      loadJobsFromStorage() {
        const storedJobs = localStorage.getItem('jobs');
        if (storedJobs) {
          this.jobs = JSON.parse(storedJobs);
        }
      },

      scrapeJobs() {
        this.scrapingInProgress = true;
        fetch("/scrape/")
          .then((response) => response.json())
          .then((data) => {
            const newJobs = data.map((job) => ({
              date: job.date,
              website: job.website,
              title: job.job_title,
              company: job.company,
              city: job.city,
              link: job.link_offer,
            }));
            this.updateJobsWithNoDuplicates(newJobs);
            this.scrapingInProgress = false;
          })
          .catch((error) => {
            console.error("Error:", error);
            this.scrapingInProgress = false;
          });
      },

      updateJobsWithNoDuplicates(newJobs) {
        const currentJobsMap = new Map(this.jobs.map(job => [job.link, job]));
        newJobs.forEach(job => {
          if (!currentJobsMap.has(job.link)) {
            this.jobs.unshift(job);
            currentJobsMap.set(job.link, job);
          }
        });
        localStorage.setItem('jobs', JSON.stringify(this.jobs));
      },

      downloadFile(url) {
        window.location.href = url;
      },

      get uniqueWebsites() {
        const websites = this.jobs.map(job => job.website);
        return [...new Set(websites)];
      },

      get filteredJobs() {
        if (this.selectedWebsite === '') {
          return this.jobs;
        }
        return this.jobs.filter(job => job.website === this.selectedWebsite);
      },
    }));
  });
