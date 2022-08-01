% Create confusion matrix

predict_file = 'eval_all.txt';
groundtruth_file = 'eval_all_groundtruth.txt';

predict_data = readcell(predict_file);
groundtruth_data = readcell(groundtruth_file);

predict_label = categorical(predict_data(:,3));
groundtruth_label = categorical(groundtruth_data(:,3));

cm = confusionmat(groundtruth_label,predict_label,"Order",{'Person', 'Empty Scence'});

cm_chart = confusionchart(cm, {'Person', 'non-Person'})
%cm.Title = 'Evaluation of person vs non-person situation';