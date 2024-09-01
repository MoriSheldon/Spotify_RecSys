import argparse
import torch
from tqdm import tqdm
import data_loader.data_loaders as module_data
import model.model as module_arch
from parse_config import ConfigParser
import pandas as pd


def main(config):
    logger = config.get_logger('test')

    # setup data_loader instances
    data_loader = getattr(module_data, config['data_loader']['type'])(
        config['data_loader']['args']['data_dir'],
        batch_size=512,
        shuffle=False,
        validation_split=0.0,
        training=False,
        num_workers=2
    )

    # build model architecture
    model = config.init_obj('arch', module_arch)
    logger.info(model)

    logger.info('Loading checkpoint: {} ...'.format(config.resume))
    checkpoint = torch.load(config.resume)
    state_dict = checkpoint['state_dict']
    if config['n_gpu'] > 1:
        model = torch.nn.DataParallel(model)
    model.load_state_dict(state_dict)

    # prepare model for testing
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)

    # start prediction
    model.eval()
    predictions =[]
    ids = []
    with torch.no_grad():
        for data, id in tqdm(data_loader):
            data = data.to(device)
            output = model(data)
            reconstruction_error = torch.sum((output - data)**2, dim=1).cpu().numpy()
            predictions.extend(reconstruction_error.tolist())
            ids.extend(id)

    # 예측 결과 저장
    sample_data = pd.read_csv("data/sample/sample.csv")
    sample_data['reconstruction_error'] = predictions
    sample_data['id'] = ids
    
    # 재구성 오차가 낮은 순으로 정렬 (낮을수록 더 좋은 추천)
    sample_data_sorted = sample_data.sort_values('reconstruction_error')
    
    # 상위 50개 항목 선택
    top_50 = sample_data_sorted.head(50)

    # 결과 저장
    top_50.to_csv('top_50_recommendations.csv', index=False)
    sample_data_sorted.to_csv('all_predictions.csv', index=False)

    logger.info('Predictions saved to all_predictions.csv')
    logger.info('Top 50 recommendations saved to top_50_recommendations.csv')


if __name__ == '__main__':
    args = argparse.ArgumentParser(description='PyTorch Template')
    args.add_argument('-c', '--config', default=None, type=str,
                      help='config file path (default: None)')
    args.add_argument('-r', '--resume', default=None, type=str,
                      help='path to latest checkpoint (default: None)')
    args.add_argument('-d', '--device', default=None, type=str,
                      help='indices of GPUs to enable (default: all)')

    config = ConfigParser.from_args(args)
    main(config)
