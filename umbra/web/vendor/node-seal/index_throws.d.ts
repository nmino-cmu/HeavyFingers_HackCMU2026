import { type MainModule } from './seal_throws.js';
export type * from './seal_throws.js';
export interface InitializeOptions {
    locateFile?: (path: string) => string;
    [key: string]: any;
}
export declare function initialize(options?: InitializeOptions): Promise<MainModule>;
export default initialize;
//# sourceMappingURL=index_throws.d.ts.map