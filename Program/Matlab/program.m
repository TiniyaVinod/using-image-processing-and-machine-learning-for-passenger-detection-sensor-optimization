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


video_path = 'human_sit-4.mp4';


detector = vision.ForegroundDetector(...
       'NumTrainingFrames', 20, ...
       'InitialVariance', 30*30);
   
   
blob = vision.BlobAnalysis(...
       'CentroidOutputPort', false, 'AreaOutputPort', false, ...
       'BoundingBoxOutputPort', true, ...
       'MinimumBlobAreaSource', 'Property', 'MinimumBlobArea', 1000);   
   
shapeInserter = vision.ShapeInserter('BorderColor','White');
   
v = VideoReader(video_path);

prev_frame = [];

while hasFrame(v)
    
    frameRGB = readFrame(v);
    frameRGB = imresize(frameRGB, frame_asp_ratio);
    frameGray = rgb2gray(frameRGB);

    out = imabsdiff(frameGray, ref_img);
    subplot 221, imshow(out), title('imabsdiff');
    
    t = graythresh(out);
    out_t = imbinarize(out, 0.35);
    subplot 222, imshow(out_t), title('imbinarize');
    
%     if ~isempty(prev_frame)
%         out = imabsdiff(frameGray, prev_frame);
%         imshow(out);
%     end
    
    fgMask = detector(out);    
    bbox   = blob(fgMask);
    out_detector   = shapeInserter(frameGray,bbox);
    subplot 223, imshow(out_detector), title('foreground_detector');
    drawnow;
end