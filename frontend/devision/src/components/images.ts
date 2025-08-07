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
