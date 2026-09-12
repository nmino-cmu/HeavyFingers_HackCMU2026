// TypeScript bindings for emscripten-generated code.  Automatically generated at compile time.
interface WasmModule {
}

type EmbindString = ArrayBuffer|Uint8Array|Uint8ClampedArray|Int8Array|string;
export interface ClassHandle {
  isAliasOf(other: ClassHandle): boolean;
  delete(): void;
  deleteLater(): this;
  isDeleted(): boolean;
  // @ts-ignore - If targeting lower than ESNext, this symbol might not exist.
  [Symbol.dispose](): void;
  clone(): this;
}
export interface VectorModulus extends ClassHandle {
  push_back(_0: Modulus): void;
  resize(_0: number, _1: Modulus): void;
  size(): number;
  get(_0: number): Modulus | undefined;
  set(_0: number, _1: Modulus): boolean;
}

export interface UtilHashFunction extends ClassHandle {
}

export interface ParmsIdType extends ClassHandle {
  values(): any;
}

export interface SecLevelTypeValue<T extends number> {
  value: T;
}
export type SecLevelType = SecLevelTypeValue<0>|SecLevelTypeValue<128>|SecLevelTypeValue<192>|SecLevelTypeValue<256>;

export interface ComprModeTypeValue<T extends number> {
  value: T;
}
export type ComprModeType = ComprModeTypeValue<0>|ComprModeTypeValue<1>|ComprModeTypeValue<2>;

export interface CoeffModulus extends ClassHandle {
}

export interface PlainModulus extends ClassHandle {
}

export interface Modulus extends ClassHandle {
  isZero(): boolean;
  isPrime(): boolean;
  bitCount(): number;
  setValue(_0: bigint): void;
  value(): bigint;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: EmbindString): void;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: any): void;
}

export interface EncryptionParameters extends ClassHandle {
  coeffModulus(): VectorModulus;
  plainModulus(): Modulus;
  parmsId(): ParmsIdType;
  scheme(): SchemeType;
  setCoeffModulus(_0: VectorModulus): void;
  setPlainModulus(_0: Modulus): void;
  setPolyModulusDegree(_0: number): void;
  polyModulusDegree(): number;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: EmbindString): void;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: any): void;
}

export interface EncryptionParameterQualifiers extends ClassHandle {
  securityLevel: SecLevelType;
  usingFFT: boolean;
  usingNTT: boolean;
  usingBatching: boolean;
  usingFastPlainLift: boolean;
  usingDescendingModulusChain: boolean;
  parametersSet(): boolean;
}

export interface ContextData extends ClassHandle {
  parms(): EncryptionParameters;
  parmsId(): ParmsIdType;
  qualifiers(): EncryptionParameterQualifiers;
  prevContextData(): ContextData;
  nextContextData(): ContextData;
  totalCoeffModulusBitCount(): number;
  chainIndex(): number;
}

export interface SEALContext extends ClassHandle {
  copy(): SEALContext;
  getContextData(_0: ParmsIdType): ContextData;
  keyContextData(): ContextData;
  firstContextData(): ContextData;
  lastContextData(): ContextData;
  keyParmsId(): ParmsIdType;
  firstParmsId(): ParmsIdType;
  lastParmsId(): ParmsIdType;
  assign(_0: SEALContext): void;
  parametersSet(): boolean;
  usingKeyswitching(): boolean;
  toHuman(): string;
}

export interface Evaluator extends ClassHandle {
  negate(_0: Ciphertext, _1: Ciphertext): void;
  negateInplace(_0: Ciphertext): void;
  add(_0: Ciphertext, _1: Ciphertext, _2: Ciphertext): void;
  addInplace(_0: Ciphertext, _1: Ciphertext): void;
  addPlain(_0: Ciphertext, _1: Plaintext, _2: Ciphertext): void;
  addPlainWithPool(_0: Ciphertext, _1: Plaintext, _2: Ciphertext, _3: MemoryPoolHandle): void;
  addPlainInplace(_0: Ciphertext, _1: Plaintext): void;
  addPlainInplaceWithPool(_0: Ciphertext, _1: Plaintext, _2: MemoryPoolHandle): void;
  sub(_0: Ciphertext, _1: Ciphertext, _2: Ciphertext): void;
  subInplace(_0: Ciphertext, _1: Ciphertext): void;
  subPlain(_0: Ciphertext, _1: Plaintext, _2: Ciphertext): void;
  subPlainWithPool(_0: Ciphertext, _1: Plaintext, _2: Ciphertext, _3: MemoryPoolHandle): void;
  subPlainInplace(_0: Ciphertext, _1: Plaintext): void;
  subPlainInplaceWithPool(_0: Ciphertext, _1: Plaintext, _2: MemoryPoolHandle): void;
  multiply(_0: Ciphertext, _1: Ciphertext, _2: Ciphertext): void;
  multiplyWithPool(_0: Ciphertext, _1: Ciphertext, _2: Ciphertext, _3: MemoryPoolHandle): void;
  multiplyInplace(_0: Ciphertext, _1: Ciphertext): void;
  multiplyInplaceWithPool(_0: Ciphertext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  multiplyPlain(_0: Ciphertext, _1: Plaintext, _2: Ciphertext): void;
  multiplyPlainWithPool(_0: Ciphertext, _1: Plaintext, _2: Ciphertext, _3: MemoryPoolHandle): void;
  multiplyPlainInplace(_0: Ciphertext, _1: Plaintext): void;
  multiplyPlainInplaceWithPool(_0: Ciphertext, _1: Plaintext, _2: MemoryPoolHandle): void;
  square(_0: Ciphertext, _1: Ciphertext): void;
  squareWithPool(_0: Ciphertext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  squareInplace(_0: Ciphertext): void;
  squareInplaceWithPool(_0: Ciphertext, _1: MemoryPoolHandle): void;
  relinearize(_0: Ciphertext, _1: RelinKeys, _2: Ciphertext): void;
  relinearizeWithPool(_0: Ciphertext, _1: RelinKeys, _2: Ciphertext, _3: MemoryPoolHandle): void;
  relinearizeInplace(_0: Ciphertext, _1: RelinKeys): void;
  relinearizeInplaceWithPool(_0: Ciphertext, _1: RelinKeys, _2: MemoryPoolHandle): void;
  cipherModSwitchToNext(_0: Ciphertext, _1: Ciphertext): void;
  cipherModSwitchToNextWithPool(_0: Ciphertext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  cipherModSwitchToNextInplace(_0: Ciphertext): void;
  cipherModSwitchToNextInplaceWithPool(_0: Ciphertext, _1: MemoryPoolHandle): void;
  cipherModSwitchTo(_0: Ciphertext, _1: ParmsIdType, _2: Ciphertext): void;
  cipherModSwitchToWithPool(_0: Ciphertext, _1: ParmsIdType, _2: Ciphertext, _3: MemoryPoolHandle): void;
  cipherModSwitchToInplace(_0: Ciphertext, _1: ParmsIdType): void;
  cipherModSwitchToInplaceWithPool(_0: Ciphertext, _1: ParmsIdType, _2: MemoryPoolHandle): void;
  plainModSwitchToNext(_0: Plaintext, _1: Plaintext): void;
  plainModSwitchToNextInplace(_0: Plaintext): void;
  plainModSwitchTo(_0: Plaintext, _1: ParmsIdType, _2: Plaintext): void;
  plainModSwitchToInplace(_0: Plaintext, _1: ParmsIdType): void;
  rescaleToNext(_0: Ciphertext, _1: Ciphertext): void;
  rescaleToNextWithPool(_0: Ciphertext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  rescaleToNextInplace(_0: Ciphertext): void;
  rescaleToNextInplaceWithPool(_0: Ciphertext, _1: MemoryPoolHandle): void;
  rescaleTo(_0: Ciphertext, _1: ParmsIdType, _2: Ciphertext): void;
  rescaleToWithPool(_0: Ciphertext, _1: ParmsIdType, _2: Ciphertext, _3: MemoryPoolHandle): void;
  rescaleToInplace(_0: Ciphertext, _1: ParmsIdType): void;
  rescaleToInplaceWithPool(_0: Ciphertext, _1: ParmsIdType, _2: MemoryPoolHandle): void;
  modReduceToNext(_0: Ciphertext, _1: Ciphertext): void;
  modReduceToNextWithPool(_0: Ciphertext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  modReduceToNextInplace(_0: Ciphertext): void;
  modReduceToNextInplaceWithPool(_0: Ciphertext, _1: MemoryPoolHandle): void;
  modReduceTo(_0: Ciphertext, _1: ParmsIdType, _2: Ciphertext): void;
  modReduceToWithPool(_0: Ciphertext, _1: ParmsIdType, _2: Ciphertext, _3: MemoryPoolHandle): void;
  modReduceToInplace(_0: Ciphertext, _1: ParmsIdType): void;
  modReduceToInplaceWithPool(_0: Ciphertext, _1: ParmsIdType, _2: MemoryPoolHandle): void;
  plainTransformToNtt(_0: Plaintext, _1: ParmsIdType, _2: Plaintext): void;
  plainTransformToNttWithPool(_0: Plaintext, _1: ParmsIdType, _2: Plaintext, _3: MemoryPoolHandle): void;
  plainTransformToNttInplace(_0: Plaintext, _1: ParmsIdType): void;
  plainTransformToNttInplaceWithPool(_0: Plaintext, _1: ParmsIdType, _2: MemoryPoolHandle): void;
  cipherTransformToNtt(_0: Ciphertext, _1: Ciphertext): void;
  cipherTransformToNttInplace(_0: Ciphertext): void;
  cipherTransformFromNtt(_0: Ciphertext, _1: Ciphertext): void;
  cipherTransformFromNttInplace(_0: Ciphertext): void;
  rotateColumns(_0: Ciphertext, _1: GaloisKeys, _2: Ciphertext): void;
  rotateColumnsWithPool(_0: Ciphertext, _1: GaloisKeys, _2: Ciphertext, _3: MemoryPoolHandle): void;
  rotateColumnsInplace(_0: Ciphertext, _1: GaloisKeys): void;
  rotateColumnsInplaceWithPool(_0: Ciphertext, _1: GaloisKeys, _2: MemoryPoolHandle): void;
  complexConjugate(_0: Ciphertext, _1: GaloisKeys, _2: Ciphertext): void;
  complexConjugateWithPool(_0: Ciphertext, _1: GaloisKeys, _2: Ciphertext, _3: MemoryPoolHandle): void;
  complexConjugateInplace(_0: Ciphertext, _1: GaloisKeys): void;
  complexConjugateInplaceWithPool(_0: Ciphertext, _1: GaloisKeys, _2: MemoryPoolHandle): void;
  rotateRows(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: Ciphertext): void;
  rotateRowsWithPool(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: Ciphertext, _4: MemoryPoolHandle): void;
  rotateRowsInplace(_0: Ciphertext, _1: number, _2: GaloisKeys): void;
  rotateRowsInplaceWithPool(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: MemoryPoolHandle): void;
  rotateVector(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: Ciphertext): void;
  rotateVectorWithPool(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: Ciphertext, _4: MemoryPoolHandle): void;
  rotateVectorInplace(_0: Ciphertext, _1: number, _2: GaloisKeys): void;
  rotateVectorInplaceWithPool(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: MemoryPoolHandle): void;
  applyGalois(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: Ciphertext): void;
  applyGaloisWithPool(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: Ciphertext, _4: MemoryPoolHandle): void;
  applyGaloisInplace(_0: Ciphertext, _1: number, _2: GaloisKeys): void;
  applyGaloisInplaceWithPool(_0: Ciphertext, _1: number, _2: GaloisKeys, _3: MemoryPoolHandle): void;
  exponentiate(_0: Ciphertext, _1: bigint, _2: RelinKeys, _3: Ciphertext): void;
  exponentiateWithPool(_0: Ciphertext, _1: bigint, _2: RelinKeys, _3: Ciphertext, _4: MemoryPoolHandle): void;
  exponentiateInplace(_0: Ciphertext, _1: bigint, _2: RelinKeys): void;
  exponentiateInplaceWithPool(_0: Ciphertext, _1: bigint, _2: RelinKeys, _3: MemoryPoolHandle): void;
}

export interface KSwitchKeys extends ClassHandle {
  size(): number;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: SEALContext, _1: EmbindString): void;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: SEALContext, _1: any): void;
}

export interface RelinKeys extends KSwitchKeys {
  copy(): RelinKeys;
  assign(_0: RelinKeys): void;
  getIndex(_0: number): number;
  hasKey(_0: number): boolean;
}

export interface GaloisKeys extends KSwitchKeys {
  copy(): GaloisKeys;
  assign(_0: GaloisKeys): void;
  hasKey(_0: number): boolean;
  getIndex(_0: number): number;
}

export interface SerializablePublicKey extends ClassHandle {
  saveToBase64(_0: ComprModeType): string;
  saveToArray(_0: ComprModeType): any;
}

export interface SerializableRelinKeys extends ClassHandle {
  saveToBase64(_0: ComprModeType): string;
  saveToArray(_0: ComprModeType): any;
}

export interface SerializableGaloisKeys extends ClassHandle {
  saveToBase64(_0: ComprModeType): string;
  saveToArray(_0: ComprModeType): any;
}

export interface SerializableCiphertext extends ClassHandle {
  saveToBase64(_0: ComprModeType): string;
  saveToArray(_0: ComprModeType): any;
}

export interface KeyGenerator extends ClassHandle {
  createPublicKeySerializable(): SerializablePublicKey;
  createRelinKeys(): RelinKeys;
  createRelinKeysSerializable(): SerializableRelinKeys;
  createGaloisKeys(): GaloisKeys;
  createGaloisKeysSerializable(): SerializableGaloisKeys;
  createPublicKey(): PublicKey;
  secretKey(): SecretKey;
  createGaloisKeysWithSteps(_0: any): GaloisKeys;
  createGaloisKeysSerializableWithSteps(_0: any): SerializableGaloisKeys;
}

export interface PublicKey extends ClassHandle {
  copy(): PublicKey;
  assign(_0: PublicKey): void;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: SEALContext, _1: EmbindString): void;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: SEALContext, _1: any): void;
}

export interface SecretKey extends ClassHandle {
  copy(): SecretKey;
  assign(_0: SecretKey): void;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: SEALContext, _1: EmbindString): void;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: SEALContext, _1: any): void;
}

export interface Plaintext extends ClassHandle {
  copy(): Plaintext;
  parmsId(): ParmsIdType;
  pool(): MemoryPoolHandle;
  assign(_0: Plaintext): void;
  shrinkToFit(): void;
  release(): void;
  setZero(): void;
  isZero(): boolean;
  isNttForm(): boolean;
  reserve(_0: number): void;
  resize(_0: number): void;
  capacity(): number;
  coeffCount(): number;
  significantCoeffCount(): number;
  nonzeroCoeffCount(): number;
  scale(): number;
  setScale(_0: number): void;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: SEALContext, _1: EmbindString): void;
  toString(): string;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: SEALContext, _1: any): void;
}

export interface Ciphertext extends ClassHandle {
  copy(): Ciphertext;
  parmsId(): ParmsIdType;
  pool(): MemoryPoolHandle;
  assign(_0: Ciphertext): void;
  release(): void;
  isTransparent(): boolean;
  isNttForm(): boolean;
  reserve(_0: SEALContext, _1: number): void;
  resize(_0: number): void;
  coeffModulusSize(): number;
  polyModulusDegree(): number;
  size(): number;
  sizeCapacity(): number;
  scale(): number;
  correctionFactor(): number;
  setScale(_0: number): void;
  saveToBase64(_0: ComprModeType): string;
  loadFromBase64(_0: SEALContext, _1: EmbindString): void;
  saveToArray(_0: ComprModeType): any;
  loadFromArray(_0: SEALContext, _1: any): void;
}

export interface BatchEncoder extends ClassHandle {
  slotCount(): number;
  encode(_0: any, _1: Plaintext): void;
  decodeBigInt64(_0: Plaintext): any;
  decodeBigInt64WithPool(_0: Plaintext, _1: MemoryPoolHandle): any;
  decodeBigUint64(_0: Plaintext): any;
  decodeBigUint64WithPool(_0: Plaintext, _1: MemoryPoolHandle): any;
}

export interface CKKSEncoder extends ClassHandle {
  slotCount(): number;
  encode(_0: any, _1: number, _2: Plaintext): void;
  encodeWithPool(_0: any, _1: number, _2: Plaintext, _3: MemoryPoolHandle): void;
  decodeFloat64(_0: Plaintext): any;
  decodeFloat64WithPool(_0: Plaintext, _1: MemoryPoolHandle): any;
}

export interface MemoryPoolHandle extends ClassHandle {
}

export interface MemoryManager extends ClassHandle {
}

export interface MMProf extends ClassHandle {
}

export interface MMProfGlobal extends MMProf {
  getPool(_0: bigint): MemoryPoolHandle;
}

export interface MMProfNew extends MMProf {
  getPool(_0: bigint): MemoryPoolHandle;
}

export interface MMProfFixed extends MMProf {
  getPool(_0: bigint): MemoryPoolHandle;
}

export interface MMProfThreadLocal extends MMProf {
  getPool(_0: bigint): MemoryPoolHandle;
}

export interface Encryptor extends ClassHandle {
  encryptSerializable(_0: Plaintext): SerializableCiphertext;
  encryptSerializableWithPool(_0: Plaintext, _1: MemoryPoolHandle): SerializableCiphertext;
  encryptSymmetricSerializable(_0: Plaintext): SerializableCiphertext;
  encryptSymmetricSerializableWithPool(_0: Plaintext, _1: MemoryPoolHandle): SerializableCiphertext;
  encryptZeroSerializable(): SerializableCiphertext;
  encryptZeroSerializableWithPool(_0: MemoryPoolHandle): SerializableCiphertext;
  setPublicKey(_0: PublicKey): void;
  setSecretKey(_0: SecretKey): void;
  encrypt(_0: Plaintext, _1: Ciphertext): void;
  encryptWithPool(_0: Plaintext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  encryptSymmetric(_0: Plaintext, _1: Ciphertext): void;
  encryptSymmetricWithPool(_0: Plaintext, _1: Ciphertext, _2: MemoryPoolHandle): void;
  encryptZero(_0: Ciphertext): void;
  encryptZeroWithPool(_0: Ciphertext, _1: MemoryPoolHandle): void;
}

export interface Decryptor extends ClassHandle {
  decrypt(_0: Ciphertext, _1: Plaintext): void;
  invariantNoiseBudget(_0: Ciphertext): number;
}

export interface SchemeTypeValue<T extends number> {
  value: T;
}
export type SchemeType = SchemeTypeValue<0>|SchemeTypeValue<1>|SchemeTypeValue<2>|SchemeTypeValue<3>;

interface EmbindModule {
  VectorModulus: {
    new(): VectorModulus;
  };
  UtilHashFunction: {
    hash(_0: any): any;
    hashBlockUint64Count: number;
    hashBlockByteCount: number;
  };
  ParmsIdType: {
    new(): ParmsIdType;
    new(_0: ParmsIdType): ParmsIdType;
  };
  SecLevelType: {none: SecLevelTypeValue<0>, tc128: SecLevelTypeValue<128>, tc192: SecLevelTypeValue<192>, tc256: SecLevelTypeValue<256>};
  ComprModeType: {none: ComprModeTypeValue<0>, zlib: ComprModeTypeValue<1>, zstd: ComprModeTypeValue<2>};
  CoeffModulus: {
    MaxBitCount(_0: number, _1: SecLevelType): number;
    BFVDefault(_0: number, _1: SecLevelType): VectorModulus;
    Create(_0: number, _1: any): VectorModulus;
  };
  PlainModulus: {
    Batching(_0: number, _1: number): Modulus;
    BatchingVector(_0: number, _1: any): VectorModulus;
  };
  Modulus: {
    new(_0: bigint): Modulus;
  };
  EncryptionParameters: {
    new(_0: SchemeType): EncryptionParameters;
  };
  EncryptionParameterQualifiers: {};
  ContextData: {};
  SEALContext: {
    new(_0: EncryptionParameters, _1: boolean, _2: SecLevelType): SEALContext;
  };
  Evaluator: {
    new(_0: SEALContext): Evaluator;
  };
  KSwitchKeys: {
    new(): KSwitchKeys;
  };
  RelinKeys: {
    new(): RelinKeys;
  };
  GaloisKeys: {
    new(): GaloisKeys;
  };
  SerializablePublicKey: {};
  SerializableRelinKeys: {};
  SerializableGaloisKeys: {};
  SerializableCiphertext: {};
  KeyGenerator: {
    new(_0: SEALContext): KeyGenerator;
    new(_0: SEALContext, _1: SecretKey): KeyGenerator;
  };
  PublicKey: {
    new(): PublicKey;
  };
  SecretKey: {
    new(): SecretKey;
  };
  Plaintext: {
    new(): Plaintext;
    new(_0: number): Plaintext;
    new(_0: number, _1: number): Plaintext;
    withPool(_0: MemoryPoolHandle): Plaintext;
    withCoeffCountAndPool(_0: number, _1: MemoryPoolHandle): Plaintext;
    withCapAndCoeffCountAndPool(_0: number, _1: number, _2: MemoryPoolHandle): Plaintext;
  };
  Ciphertext: {
    new(): Ciphertext;
    new(_0: SEALContext): Ciphertext;
    new(_0: SEALContext, _1: ParmsIdType): Ciphertext;
    new(_0: SEALContext, _1: ParmsIdType, _2: number): Ciphertext;
    withPool(_0: MemoryPoolHandle): Ciphertext;
    withContextAndPool(_0: SEALContext, _1: MemoryPoolHandle): Ciphertext;
    withContextAndParmsIdTypeAndPool(_0: SEALContext, _1: ParmsIdType, _2: MemoryPoolHandle): Ciphertext;
    withContextAndParmsIdTypeAndCapacityAndPool(_0: SEALContext, _1: ParmsIdType, _2: number, _3: MemoryPoolHandle): Ciphertext;
  };
  BatchEncoder: {
    new(_0: SEALContext): BatchEncoder;
  };
  CKKSEncoder: {
    new(_0: SEALContext): CKKSEncoder;
  };
  MemoryPoolHandle: {
    new(): MemoryPoolHandle;
    Global(): MemoryPoolHandle;
    ThreadLocal(): MemoryPoolHandle;
    New(_0: boolean): MemoryPoolHandle;
  };
  MemoryManager: {
    GetPool(_0: bigint): MemoryPoolHandle;
  };
  MMProf: {};
  MMProfGlobal: {};
  MMProfNew: {};
  MMProfFixed: {};
  MMProfThreadLocal: {};
  Encryptor: {
    new(_0: SEALContext, _1: PublicKey): Encryptor;
    new(_0: SEALContext, _1: PublicKey, _2: SecretKey): Encryptor;
  };
  Decryptor: {
    new(_0: SEALContext, _1: SecretKey): Decryptor;
  };
  SchemeType: {none: SchemeTypeValue<0>, bfv: SchemeTypeValue<1>, ckks: SchemeTypeValue<2>, bgv: SchemeTypeValue<3>};
  jsArrayFromVecModulus(_0: VectorModulus): any;
  vecFromArrayModulus(_0: any): VectorModulus;
}

export type MainModule = WasmModule & EmbindModule;
export default function MainModuleFactory (options?: unknown): Promise<MainModule>;
