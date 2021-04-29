import argparse
import os
import json
import operator
from curia import *


def resolve_handler(cfg):

    infra = os.getenv("INFRA")

    if infra == "AWS":
        return S3Data(cfg)
    elif infra == "GCP":
        return GCPData(cfg)
    elif infra == "AZURE":
        return AzureData(cfg)
    else:
        raise ValueError(f"Unrecognized cloud infrastructure: {infra}")


def post_data(_handler, destination_bucket: str):

    all_files = {}
    for subdir, dirs, files in os.walk("/data/"):
        for file in files:
            if file[0] != '.':
                all_files[file] = os.path.getmtime("{0}/{1}".format("/data/", file))

    # this is a hack to avoid writing all intermittent files back to the cloud.
    # it grabs the most recently modified file, which should be the output file,
    # since it is written to last
    output_file = max(all_files.items(), key=operator.itemgetter(1))[0]
    handler.put_data(destination_bucket, f"/data/{output_file}", output_file)

    return output_file


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--pull", action="store_true")
    args = parser.parse_args()

    if args.push and args.pull:
        raise Exception("Can only select either push or pull, not both.")

    if not (args.push or args.pull):
        raise Exception("Must select either push or pull")

    config = json.loads(
        open(os.getenv("STORAGE_HANDLER_CONFIG"), "r").read()
    )

    handler = resolve_handler(config)

    if args.pull:

        source_bucket = os.getenv("SOURCE_BUCKET")
        source_file = os.getenv("SOURCE_KEY")
        write_path = os.getenv("WRITE_PATH")

        handler.get_data(
            source_bucket,
            source_file,
            write_path
        )

        print(
            f"Successfully pulled file {source_file} from bucket "
            f"{source_bucket} and wrote it to disk at {write_path}."
        )

    elif args.push:

        dest_bucket = os.getenv("DESTINATION_BUCKET")
        f = post_data(handler, dest_bucket)
        print(f"Successfully wrote file {f} to bucket {dest_bucket}")

    else:
        raise Exception("Must select either push or pull.")
