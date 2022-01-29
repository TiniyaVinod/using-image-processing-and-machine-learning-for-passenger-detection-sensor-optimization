% Program to detect a human from top-view basing on Background subtraction
% (Fixed environment)
% 1.) Source selection (video or webcam)
% 2.) Import background image (fixed background)
% 3.) Acquire frames from source
% 4.) Process the frame
% 5.) Show the result

%% 1.) Source selection
% Now support only video
videoSource = VideoReader('human_sit.mp4');




detector = vision.ForegroundDetector(...
       'NumTrainingFrames', 20, ...
       'InitialVariance', 100*200);
   
blob = vision.BlobAnalysis(...
       'CentroidOutputPort', false, 'AreaOutputPort', false, ...
       'BoundingBoxOutputPort', true, ...
       'MinimumBlobAreaSource', 'Property', 'MinimumBlobArea', 250);

shapeInserter = vision.ShapeInserter('BorderColor','White');

videoPlayer = vision.VideoPlayer();

while hasFrame(videoSource)
     frame  = readFrame(videoSource);
     frame = imresize(frame, 0.1);
     fgMask = detector(frame);
     bbox   = blob(fgMask);
     out    = shapeInserter(frame,bbox);
     videoPlayer(out);
     pause(0.1);
end

release(videoPlayer);
