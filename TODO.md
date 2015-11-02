### TODO

* sliding window
* NLP pipelined: POS (1-v encoding?)
* LevelDB
* data management
* ensure valid train / test split

### Questions

* How to handle cases when ASR went wrong?
* 
  Example 1:
  PUNCTUATED:  And today, I had time to show you one point in this new design space, and a few of the possibilities that we're working to bring out of the laboratory.
  NUN_PUNCTUATED: And today had time to show you one point in this new design space and a few of the possibilities or working to bring out a laboratory

  Example 2:
  PUNCTUATED:  And now, finally, I can fade the whole sequence out using the volume Siftable, tilted to the left.
  NUN_PUNCTUATED: And now finally I can fiddle sequence out using the volumes of double tilted to the left
