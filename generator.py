from config import Config
from consts import *
import countdown
import genimg as gen
import time
import os.path as fs
from datetime import date

import log


def _timestamp():
    return time.time_ns() // 1000000000

def _format_date(d: date):
    return str(d.month) + '/' + str(d.day) + '/' + str(d.year)

class Generator:
    def __init__(self, config: Config):
        self.config = config

        self.last_days_ago = None
        self.last_edition_name = None
        self.last_edition_check = None
        self.edition = None

    def _are_files_present(self):
        config = self.config

        if not fs.exists(config.generated_path):
            return False

        for size in config.sizes:
            path = config.generated_path + BANNER_FILE_NAME + "_" + str(size) + ".png"

            if not fs.exists(path):
                return False

        return True


    def _load_edition(self):
        should_reload = False
        now = _timestamp()

        if self.edition == None:
            should_reload = True

        elif self.last_edition_check == None:
            should_reload = True

        elif now - self.last_edition_check > 60:
            should_reload = True

        if not should_reload:
            return



        log.debug("Re-fetching edition info")

        self.last_edition_check = now

        config = self.config

        # If customized dates are configured, prefer those over URL so that these can easily
        # override the URL in debug cases
        if config.edition_name != None and config.start_date != None and config.end_date != None:
            self.edition = countdown.Edition(
                config.edition_name,
                config.start_date,
                config.end_date
            )
        else:
            self.edition = countdown.load_edition(config.edition_url)


    def _should_generate(self) -> bool:
        if not self._are_files_present():
            return True

        edname = self.edition.name
        eddays = self.edition.days_difference()

        if edname != self.last_edition_name:
            return True

        if eddays != self.last_days_ago:
            return True

        return False


    def generate(self):
        self._load_edition()

        if not self._should_generate():
            log.debug("Not generating images as they are up to date")
            return
        
        self.last_edition_name = self.edition.name
        self.last_days_ago = self.edition.days_difference()

        log.info("Regenerating banner images")

        config = self.config
        gen.generate(
            self.edition.name,
            self.edition.format_text(),
            assets_path=config.assets_path,
            generated_path=config.generated_path
        )

    def generate_info(self):
        self._load_edition()

        d = {
            'edition': self.edition.name,
            'start': _format_date(self.edition.start),
            'end': _format_date(self.edition.end),
        }

        diff = self.edition.days_difference()
        d['message'] = self.edition.format_text()
        d['diff'] = diff
        d['now'] = (diff == 0)

        if diff > 0:
            d['days_until'] = diff

        if diff < 0:
            d['days_ago'] = -diff

        return d
