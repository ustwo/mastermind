//
//  ViewController.swift
//  testMastermind
//
//  Created by Jarod on 12/01/2016.
//  Copyright © 2016 ustwo. All rights reserved.
//

import UIKit

class ViewController: UIViewController {
    
    @IBOutlet var path: UITextField?
    @IBOutlet var textView: UITextView?
    @IBOutlet weak var sendToMastermind: UIButton!
    
    override func viewDidLoad() {
        super.viewDidLoad()
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
    }

    @IBAction func sendRequestToMastermind(sender: AnyObject) {
        
        sendToMastermind.enabled = false
        
        if let address = path?.text {
            if let url = NSURL(string: "http://proxapp:5000/\(address)") {
                print(url)

                let request = NSMutableURLRequest(URL: url)
                let config = NSURLSessionConfiguration.ephemeralSessionConfiguration()
                
                let session = NSURLSession(configuration: config)
                
                request.HTTPMethod = "GET"
                
                let task = session.dataTaskWithRequest(request, completionHandler: { (data, response, error) -> Void in
                    
                    dispatch_async(dispatch_get_main_queue(), { () -> Void in
                        
                        self.sendToMastermind.enabled = true
                        
                        if let errorMessage = error?.localizedDescription {
                            self.textView?.text? = errorMessage
                        } else {
                            let datastring = NSString(data: data!, encoding: NSUTF8StringEncoding)
                            print(datastring!)
                        }
                    })
                })

                task.resume()
                
            } else {
                
                showAlert()
            }
  
        } else {
            
            showAlert()
        }
    }
    
    func showAlert() {
        
        let alert = UIAlertController(title: "IP Address", message: "Please provide an IP address for mastermind", preferredStyle: .Alert)
        alert.addAction(UIAlertAction(title: "OK", style: .Default, handler: nil))
        self.presentViewController(alert, animated: true, completion: nil)
    }
}

