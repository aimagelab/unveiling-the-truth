import pickle
import argparse
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import numpy as np


def parse_args():
    parser = argparse.ArgumentParser(description="Visualize scanpath data")
    parser.add_argument("--img_id", type=str, help="Id of the image to visualize")
    parser.add_argument(
        "--type",
        type=str,
        choices=[
            "original",
            "semantic_aware",
            "semantic_agnostic",
            "pix2pix_magicbrush",
        ],
        help="Type of edting",
    )
    parser.add_argument("--user", type=int, help="User id to visualize")
    parser.add_argument(
        "--output_raw_file",
        default="output_raw.png",
        type=str,
        help="Output file to save raw saccades and fixations",
    )
    parser.add_argument(
        "--output_fixations_file",
        type=str,
        default="output_fixations.png",
        help="Output file to save processed fixations",
    )
    return parser.parse_args()


def visualize_raw_saccades_and_fixations(data, img_id, type, user):
    scanpath_info = data[img_id][type]["user_" + str(user)]

    im = plt.imread(f"dataset/images/{type}/{img_id}.jpg")
    fig = plt.figure()
    plt.imshow(im)
    plt.scatter(scanpath_info["x_coords"], scanpath_info["y_coords"], c="red", s=1)

    plt.savefig(args.output_raw_file)
    plt.close()


def plot_scanpath(data, img_id, type, user) -> None:
    scanpath_info = data[img_id][type]["user_" + str(user)]

    im = Image.open(f"dataset/images/{args.type}/{args.img_id}.jpg")
    xs = scanpath_info["x_fix"]
    ys = scanpath_info["y_fix"]

    im = np.asarray(im)
    if len(im.shape) == 2:
        im = np.repeat(np.expand_dims(im, axis=2), 3, axis=2)

    fig, ax = plt.subplots()
    ax.imshow(im)

    for i in range(len(xs)):
        if i > 0:
            plt.plot(
                [xs[i - 1], xs[i]],
                [ys[i - 1], ys[i]],
                color="green",
                linewidth=1.5,
                alpha=0.5,
            )

    for i in range(len(xs)):
        facecolor = "red" if i == 0 else "blue" if i == len(xs) - 1 else "white"

        circle = plt.Circle(
            (xs[i], ys[i]), radius=10, edgecolor="black", facecolor=facecolor, alpha=0.5
        )
        ax.add_patch(circle)

    save_path = args.output_fixations_file
    plt.savefig(save_path)
    plt.close()

def main(args):
    with open("dataset/gaze_data.pickle", "rb") as fp:
        data = pickle.load(fp)

    visualize_raw_saccades_and_fixations(data, args.img_id, args.type, args.user)
    plot_scanpath(data, args.img_id, args.type, args.user)

if __name__ == "__main__":
    args = parse_args()
    main(args)