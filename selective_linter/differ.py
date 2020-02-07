import pydriller


class Differ(pydriller.git_repository.GitRepository):
    # def get_diffs(self):
    #     print(f"Currently on branch {self.head.ref.name}")
    #     diffs = self.index.diff(None) + self.index.diff('HEAD')
    #     blobs = [(diff.a_blob, diff.b_blob) for diff in diffs]
    #     filenames = [blob.path for (blob, _) in blobs]
