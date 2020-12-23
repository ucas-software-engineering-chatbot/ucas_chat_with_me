import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from imageio import imread
plt.rcParams['font.size'] = 6
plt.rcParams['figure.figsize'] = (10,2.5)

def check_test_result():
    for k in range(5):
        x = imread("test_data/noface"+str(k+1)+".jpg") / 255.
        # y = labels_df[labels_df.Filename==test_files[i]].score.values
        plt.subplot(1, 5, k+1)
        plt.imshow(x)
        # plt.title("p:%.2f a:%.2f" % (predicted[0][0], y))
        plt.axis('off')
    plt.savefig('noFaces.jpg')

check_test_result()