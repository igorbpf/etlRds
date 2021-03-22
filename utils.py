import csv


class DictReaderStrip(csv.DictReader):
    @property
    def fieldnames(self):
        if self._fieldnames is None:
            # Initialize self._fieldnames
            # Note: DictReader is an old-style class, so can't use super()
            csv.DictReader.fieldnames.fget(self)
            if self._fieldnames is not None:
                self._fieldnames = [name.strip() for name in self._fieldnames]
        return self._fieldnames


if __name__ == "__main__":

    data = []

    with open("./data.csv") as csvfile:
        reader = DictReaderStrip(csvfile)
        for row in reader:
            # print(row.keys())
            print(row["agencia"])


print(data)
