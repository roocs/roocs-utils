import os

from roocs_utils import CONFIG
from roocs_utils.inventory import logging
from roocs_utils.inventory.utils import create_dir

LOGGER = logging.getLogger(__file__)


class BatchManager(object):
    def __init__(self, project):
        self._project = project
        self._proj_conf = CONFIG[f"project:{self._project}"]

        self._batch_dir = os.path.join(self._proj_conf["inventory_dir"], "batches")
        create_dir(self._batch_dir)

    def get_batch_files(self):
        batch_files = []

        for batch_file in sorted(os.listdir(self._batch_dir)):

            batch_file_path = os.path.join(self._batch_dir, batch_file)
            batch_files.append(batch_file_path)

        return batch_files

    def get_batches(self):
        for batch_file_path in self.get_batch_files():
            yield open(batch_file_path).read().strip().split()

    def get_batch(self, batch_number):
        batch_file_path = self.get_batch_files()[batch_number - 1]
        return open(batch_file_path).read().strip().split()

    def batch_file_to_batch_number(self, batch_file):
        return int(os.path.basename(batch_file).split("_")[-1].split(".")[0])

    def _write_batch(self, batch_number, batch):
        batch_file = os.path.join(self._batch_dir, f"batch_{batch_number:04d}.txt")

        with open(batch_file, "w") as writer:
            writer.write("\n".join(batch))

        LOGGER.debug(f"Wrote batch file: {batch_file}")

    def create_batches(self):
        # Read in all datasets
        datasets_file = self._proj_conf["datasets_file"]
        self._datasets = open(datasets_file).read().strip().split()

        # Loop through grouping them into batches of n_per_batch
        # - write each batch to text file in versioned data directory
        n_per_batch = CONFIG["workflow"]["n_per_batch"]
        current_batch = []
        batch_count = 1

        for count, dataset_id in enumerate(self._datasets):
            current_batch.append(dataset_id)

            if count > 0 and count % n_per_batch == 0:
                self._write_batch(batch_count, current_batch)

                # Update variables
                current_batch = []
                batch_count += 1

        # Write last one if not written
        if current_batch:
            self._write_batch(batch_count, current_batch)

        LOGGER.info(f"Wrote {batch_count} batch files.")
