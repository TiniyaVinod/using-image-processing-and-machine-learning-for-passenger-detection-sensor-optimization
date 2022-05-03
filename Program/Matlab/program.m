% Program to detect a human from top-view basing on Background subtraction
% (Fixed environment)
% 0.) Parameter Setting
% 1.) Source Selection (video or webcam)
% 2.) Background subtraction



%% 0.) Parameter Setting
data_path = "..\..\Data\Videos";
data_filetype = ".png";
frame_asp_ratio = [128 128];

ref_img = imread('ref.jpg');
ref_img = imresize(ref_img, frame_asp_ratio);
ref_img = rgb2gray(ref_img);


video_path = 'human_stand.mp4';

detector = vision.ForegroundDetector(...
       'NumTrainingFrames', 20, ...
       'InitialVariance', 30*30);
   
   
blob = vision.BlobAnalysis(...
       'CentroidOutputPort', false, 'AreaOutputPort', false, ...
       'BoundingBoxOutputPort', true, ...
       'MinimumBlobAreaSource', 'Property', 'MinimumBlobArea', 1000, ...
       'MaximumCount', 1);   
   
shapeInserter = vision.ShapeInserter('BorderColor','White');
   
v = VideoReader(video_path);

prev_frame = [];



model = load('cnn_model.mat','-mat');
model = model.model;



while hasFrame(v)
    
    frameRGB = readFrame(v);
    frameRGB = imresize(frameRGB, frame_asp_ratio);
    frameGray = rgb2gray(frameRGB);
     
    [YPred, scores] = classify(model, frameRGB);

    tmp = cellstr(YPred);

    subplot 111, imshow(frameRGB), title(tmp{1})
    drawnow;
    
end