from typing import Optional
class ListNode:
      def __init__(self,val=0,next=None):
        self.val=val
        self.next=next
class Solution:
    def removeNthFromEnd(self,head:Optional[ListNode],n:int) ->Optional[ListNode]:
        dummy=ListNode(0,head)
        result=dummy
        fast=head
        
        for i in range(0,n):
            fast=fast.next
        while fast: 
            result=result.next 
            fast=fast.next
        
        result.next=result.next.next
        return dummy.next
        
           

