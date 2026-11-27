/**
 * Tripo (tripo) — generated from the platform OpenAPI spec.
 *
 * Do not edit by hand: run `python scripts/generate_providers.py`. Parameter
 * names, types, enums and required-ness all come from the live spec.
 */

import { Transport } from '../../runtime/transport';
import { TaskHandle } from '../../runtime/tasks';


function taskId(result: Record<string, unknown>): string {
  if (typeof result?.task_id === 'string') return result.task_id;
  const data = result?.data as Record<string, unknown> | undefined;
  if (data && typeof data.task_id === 'string') return data.task_id;
  return typeof result?.id === 'string' ? result.id : '';
}

export interface TripoGenerateOptions {
  action?: "generate";
  model?: "v3.1-20260211" | "v3.0-20250812" | "v2.5-20250123" | "P1-20260311" | "P2-20260801";
  texture?: "none" | "standard";
  prompt?: string;
  /** Public PNG or JPEG up to 20 MiB. */
  imageUrl?: string;
  /** Front, left, back, right. Front and at least one other image are required. Use null to skip an optional view. */
  imageUrls?: (string | null)[];
  idempotencyKey?: string;
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TripoModelsOptions {
  action: "import" | "texture" | "convert";
  /** Public HTTPS URL to a supported model file up to 150 MiB. */
  modelUrl?: string;
  modelId?: string;
  model?: "v3.5-20260815" | "v3.0-20250812" | "v2.5-20250123";
  textureQuality?: "fast" | "standard" | "detailed" | "extreme";
  textureAlignment?: "original_image" | "geometry";
  textureSeed?: number;
  pbr?: boolean;
  bake?: boolean;
  delight?: boolean;
  partNames?: string[];
  compress?: "geometry";
  prompt?: string;
  /** Public PNG or JPEG up to 20 MiB. */
  imageUrl?: string;
  /** Front, left, back, right. Front and at least one other image are required. Use null to skip an optional view. */
  imageUrls?: (string | null)[];
  /** Public PNG or JPEG up to 20 MiB. */
  styleImageUrl?: string;
  format?: "GLTF" | "FBX" | "USDZ" | "OBJ" | "STL" | "3MF";
  quad?: boolean;
  forceSymmetry?: boolean;
  flattenBottom?: boolean;
  packUv?: boolean;
  exportVertexColors?: boolean;
  pivotToCenterBottom?: boolean;
  withAnimation?: boolean;
  animateInPlace?: boolean;
  faceLimit?: number;
  flattenBottomThreshold?: number;
  textureSize?: number;
  textureFormat?: "JPEG" | "PNG" | "WEBP" | "BMP";
  scaleFactor?: number;
  exportOrientation?: "+x" | "-x" | "+y" | "-y";
  fbxPreset?: "blender" | "3dsmax" | "mixamo" | "bake_scale";
  texturePackaging?: "embedded" | "zip";
  idempotencyKey?: string;
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TripoAnimationsOptions {
  action: "rig_check" | "rig" | "retarget";
  modelId?: string;
  /** Public HTTPS URL to a supported model file up to 150 MiB. */
  modelUrl?: string;
  model?: "v1.0-20240301" | "v2.5-20260210" | "v3.0-20260909";
  rigType?: "biped" | "quadruped" | "hexapod" | "octopod" | "avian" | "serpentine" | "aquatic" | "others";
  spec?: "tripo" | "mixamo" | "actorcore" | "unity" | "unreal" | "vrm";
  format?: "GLB" | "FBX";
  animation?: string;
  animations?: string[];
  exportWithGeometry?: boolean;
  animateInPlace?: boolean;
  idempotencyKey?: string;
  /** Submit asynchronously and poll. Defaults to true. */
  async?: boolean;
  /** Wait for completion before returning the handle. */
  wait?: boolean;
  pollInterval?: number;
  maxWait?: number;
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

export interface TripoTasksOptions {
  action?: "retrieve" | "retrieve_batch";
  id?: string;
  traceId?: string;
  ids?: string[];
  traceIds?: string[];
  callbackUrl?: string;
  /** Any parameter added upstream before the SDK is regenerated. */
  [key: string]: unknown;
}

/** tripo client. */
export class Tripo {
  constructor(private transport: Transport) {}

  /** Tripo Generations */
  async generate(options: TripoGenerateOptions = {}): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action ?? "generate";
    body["model"] = options.model ?? "v3.1-20260211";
    body["texture"] = options.texture ?? "standard";
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "idempotencyKey", "imageUrl", "imageUrls", "maxWait", "model", "pollInterval", "prompt", "texture", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/tripo/generations", { json: body, headers: options.idempotencyKey !== undefined ? {"Idempotency-Key": options.idempotencyKey} : {} })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/tripo/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Tripo Models */
  async models(options: TripoModelsOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    if (options.modelUrl !== undefined) body["model_url"] = options.modelUrl;
    if (options.modelId !== undefined) body["model_id"] = options.modelId;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.textureQuality !== undefined) body["texture_quality"] = options.textureQuality;
    if (options.textureAlignment !== undefined) body["texture_alignment"] = options.textureAlignment;
    if (options.textureSeed !== undefined) body["texture_seed"] = options.textureSeed;
    if (options.pbr !== undefined) body["pbr"] = options.pbr;
    if (options.bake !== undefined) body["bake"] = options.bake;
    if (options.delight !== undefined) body["delight"] = options.delight;
    if (options.partNames !== undefined) body["part_names"] = options.partNames;
    if (options.compress !== undefined) body["compress"] = options.compress;
    if (options.prompt !== undefined) body["prompt"] = options.prompt;
    if (options.imageUrl !== undefined) body["image_url"] = options.imageUrl;
    if (options.imageUrls !== undefined) body["image_urls"] = options.imageUrls;
    if (options.styleImageUrl !== undefined) body["style_image_url"] = options.styleImageUrl;
    if (options.format !== undefined) body["format"] = options.format;
    if (options.quad !== undefined) body["quad"] = options.quad;
    if (options.forceSymmetry !== undefined) body["force_symmetry"] = options.forceSymmetry;
    if (options.flattenBottom !== undefined) body["flatten_bottom"] = options.flattenBottom;
    if (options.packUv !== undefined) body["pack_uv"] = options.packUv;
    if (options.exportVertexColors !== undefined) body["export_vertex_colors"] = options.exportVertexColors;
    if (options.pivotToCenterBottom !== undefined) body["pivot_to_center_bottom"] = options.pivotToCenterBottom;
    if (options.withAnimation !== undefined) body["with_animation"] = options.withAnimation;
    if (options.animateInPlace !== undefined) body["animate_in_place"] = options.animateInPlace;
    if (options.faceLimit !== undefined) body["face_limit"] = options.faceLimit;
    if (options.flattenBottomThreshold !== undefined) body["flatten_bottom_threshold"] = options.flattenBottomThreshold;
    if (options.textureSize !== undefined) body["texture_size"] = options.textureSize;
    if (options.textureFormat !== undefined) body["texture_format"] = options.textureFormat;
    if (options.scaleFactor !== undefined) body["scale_factor"] = options.scaleFactor;
    if (options.exportOrientation !== undefined) body["export_orientation"] = options.exportOrientation;
    if (options.fbxPreset !== undefined) body["fbx_preset"] = options.fbxPreset;
    if (options.texturePackaging !== undefined) body["texture_packaging"] = options.texturePackaging;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "animateInPlace", "async", "bake", "callbackUrl", "compress", "delight", "exportOrientation", "exportVertexColors", "faceLimit", "fbxPreset", "flattenBottom", "flattenBottomThreshold", "forceSymmetry", "format", "idempotencyKey", "imageUrl", "imageUrls", "maxWait", "model", "modelId", "modelUrl", "packUv", "partNames", "pbr", "pivotToCenterBottom", "pollInterval", "prompt", "quad", "scaleFactor", "styleImageUrl", "textureAlignment", "textureFormat", "texturePackaging", "textureQuality", "textureSeed", "textureSize", "wait", "withAnimation"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/tripo/models", { json: body, headers: options.idempotencyKey !== undefined ? {"Idempotency-Key": options.idempotencyKey} : {} })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/tripo/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Tripo Animations */
  async animations(options: TripoAnimationsOptions): Promise<TaskHandle> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action;
    if (options.modelId !== undefined) body["model_id"] = options.modelId;
    if (options.modelUrl !== undefined) body["model_url"] = options.modelUrl;
    if (options.model !== undefined) body["model"] = options.model;
    if (options.rigType !== undefined) body["rig_type"] = options.rigType;
    if (options.spec !== undefined) body["spec"] = options.spec;
    if (options.format !== undefined) body["format"] = options.format;
    if (options.animation !== undefined) body["animation"] = options.animation;
    if (options.animations !== undefined) body["animations"] = options.animations;
    if (options.exportWithGeometry !== undefined) body["export_with_geometry"] = options.exportWithGeometry;
    if (options.animateInPlace !== undefined) body["animate_in_place"] = options.animateInPlace;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "animateInPlace", "animation", "animations", "async", "callbackUrl", "exportWithGeometry", "format", "idempotencyKey", "maxWait", "model", "modelId", "modelUrl", "pollInterval", "rigType", "spec", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    body.async = options.async ?? true;
    const result = (await this.transport.request('POST', "/tripo/animations", { json: body, headers: options.idempotencyKey !== undefined ? {"Idempotency-Key": options.idempotencyKey} : {} })) as Record<string, unknown>;
    const handle = new TaskHandle(taskId(result), "/tripo/tasks", this.transport, result);
    if (options.wait) {
      await handle.wait({ pollInterval: options.pollInterval, maxWait: options.maxWait });
    }
    return handle;
  }

  /** Tripo tasks */
  async tasks(options: TripoTasksOptions = {}): Promise<Record<string, unknown>> {
    const body: Record<string, unknown> = {};
    body["action"] = options.action ?? "retrieve";
    if (options.id !== undefined) body["id"] = options.id;
    if (options.traceId !== undefined) body["trace_id"] = options.traceId;
    if (options.ids !== undefined) body["ids"] = options.ids;
    if (options.traceIds !== undefined) body["trace_ids"] = options.traceIds;
    for (const [key, value] of Object.entries(options)) {
      if (!["action", "async", "callbackUrl", "id", "ids", "maxWait", "pollInterval", "traceId", "traceIds", "wait"].includes(key) && value !== undefined) {
        body[key] = value;
      }
    }
    if (options.callbackUrl !== undefined) body.callback_url = options.callbackUrl;
    return (await this.transport.request('POST', "/tripo/tasks", { json: body })) as Record<string, unknown>;
  }

}
