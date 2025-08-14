export interface images{
    filename: string;
    index: number;
    url: string;
}

export interface predictions extends images{
    prediction?: number;
    classification?: boolean;
    classification_prediction?: number;
}

export interface oyster_predictions extends images{
    prediction?: number;
    model?: string;
    sizeClass?: string;
    seedTrayWeight?: number;
    slideWeight?: number;
    combinedWeight?: number;
    subSample?: number;
    total?: number;
}
