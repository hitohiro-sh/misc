//
//  main.swift
//  HelloMetal
//
//  Created by hitohiro-sh on 2022/03/21.
//

import Foundation
import Metal

let arrayLength = 1 << 24
let bufferSize = arrayLength * MemoryLayout<Float32>.size

class MetalAdder {
    let device : MTLDevice // = MTLCreateSystemDefaultDevice()!
    var _mAddFunctionPSO : MTLComputePipelineState?
    var _mCommandQueue : MTLCommandQueue?

    var _mBufferA : MTLBuffer?
    var _mBufferB : MTLBuffer?
    var _mBufferResult : MTLBuffer?
    
    init(_ device : MTLDevice) {
        self.device = device
        _mAddFunctionPSO = nil
        _mCommandQueue = nil
        _mBufferA = nil
        _mBufferB = nil
        _mBufferResult = nil
    }
    
    func prepareData() {

        if let defaultLibrary = device.makeDefaultLibrary() {
            if let addFunction = defaultLibrary.makeFunction(name: defaultLibrary.functionNames[0]) {
                do {
                    _mAddFunctionPSO = try device.makeComputePipelineState(function: addFunction)
                } catch {
                    print("Failed.")
                    exit(0)
                }
            } else {
                print("Failed to find the adder function.")
                exit(0)
            }
            _mCommandQueue = device.makeCommandQueue()!
            
            _mBufferA = device.makeBuffer(length: bufferSize, options: MTLResourceOptions.storageModeShared)
            _mBufferB = device.makeBuffer(length: bufferSize, options: MTLResourceOptions.storageModeShared)
            _mBufferResult = device.makeBuffer(length: bufferSize, options: MTLResourceOptions.storageModeShared)
            
            
            // UnsafeMutableRawPointer<Float32>
            if let dataPtr = _mBufferA?.contents() {
                for index in 0..<arrayLength {
                    dataPtr.advanced(by: MemoryLayout<Float32>.alignment * index).storeBytes(of: Float32.random(in: 0...1.0), as: Float32.self)
                }
            }
            if let dataPtr2 = _mBufferB?.contents() {
                for index in 0..<arrayLength {
                    dataPtr2.advanced(by: 4 * index).storeBytes(of: Float32.random(in: 0...1.0), as: Float32.self)
                }
            }
            
        } else {
            print("Failed to find the default library.")
            exit(0)
        }
    }
        
    func sendComputeCommand() {
        let commandBuffer = _mCommandQueue!.makeCommandBuffer()!
        let computeEncoder = commandBuffer.makeComputeCommandEncoder()!
        
        computeEncoder.setComputePipelineState(_mAddFunctionPSO!)
        computeEncoder.setBuffer(_mBufferA, offset: 0, index: 0)
        computeEncoder.setBuffer(_mBufferB, offset: 0, index: 1)
        computeEncoder.setBuffer(_mBufferResult, offset: 0, index: 2)
        
        let gridSize = MTLSize(width: arrayLength, height: 1, depth: 1)
        var threadGroupSize = _mAddFunctionPSO!.maxTotalThreadsPerThreadgroup
        if (threadGroupSize > arrayLength) {
            threadGroupSize = arrayLength
        }
        let threadgroupSize = MTLSize(width: threadGroupSize, height: 1, depth: 1)
        
        computeEncoder.dispatchThreads(gridSize, threadsPerThreadgroup: threadgroupSize)
        
        computeEncoder.endEncoding()
        commandBuffer.commit()
        
        commandBuffer.waitUntilCompleted();
        
        // _mBufferA!.contents().bindMemory(to: Float32.self, capacity: arrayLength).assign(from: _mBufferResult!.contents().bindMemory(to: Float32.self, capacity: arrayLength), count: arrayLength)
        
        let a = _mBufferA?.contents()
        let b = _mBufferB?.contents()
        let result = _mBufferResult?.contents()
        
        for index in 0..<arrayLength {
            let vr = result!.advanced(by: MemoryLayout<Float32>.alignment * index).load(as: Float32.self)
            let va = a!.advanced(by: MemoryLayout<Float32>.alignment * index).load(as: Float32.self)
            let vb = b!.advanced(by: MemoryLayout<Float32>.alignment * index).load(as: Float32.self)
            if vr != va + vb {
                print(String(format: "Compute ERROR: index=%lu result=%g vs %g=a+b\n",
                       index, vr, va + vb))
            }
        }
        print("Compute results as expected\n")
        
    }
}

func main() {
    let device = MTLCreateSystemDefaultDevice()
    
    let adder = MetalAdder(device!)
    adder.prepareData()
    adder.sendComputeCommand()
    
    print("Execution finished")
}

main()
