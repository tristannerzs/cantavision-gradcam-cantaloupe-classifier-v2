# Student Presentation Script

Good day. This is my final website deployment for my binary cantaloupe image classification project.

The title of my project is **CantaVision Grad-CAM Studio: A Web-Deployed Cantaloupe Classification System Using Transfer Learning, Region-of-Interest Cropping, and Interactive Model Explainability**.

I made this website to show how my trained model can be used in a real browser-based application. A user can upload an image of fruit and choose either full-image prediction or region-of-interest prediction. ROI prediction is useful when an image contains multiple fruits because the user can move the orange crop box onto the exact fruit or area that should be classified.

After prediction, the selected crop is resized to 224 by 224 pixels, which matches the model input size used during training. The model outputs the probability that the selected crop is a cantaloupe. The website then applies the selected confidence threshold to decide whether the final label is cantaloupe or not_cantaloupe.

The website also includes Grad-CAM explainability. It shows a blocky jet-style heatmap similar to the heatmap outputs from my notebook. Red and yellow areas show stronger model focus, while blue areas show weaker activation. I also included an overlay and a notebook-style study panel with original image, Grad-CAM heatmap, and overlay.

For interactivity, I added a movable Grad-CAM studio. In this section, the heatmap can be dragged, resized, masked, and adjusted using sliders. This helps explain how the model focuses on image regions.

Finally, every prediction is saved in a SQLite database, and the results can be exported as CSV. This makes the project more complete as a deployable academic machine learning application.
