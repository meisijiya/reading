---
uid: 14
level: 1
chapterNumber: §14
title: 第14章 资源与调度
wordCount: 12040
parentPart: 第四部分
---

## 第14章 资源与调度

调度是容器编排系统最核心的功能之一，“编排”一词本身便包含“调度”的含义。调度是指为新创建的Pod找到一个最恰当的宿主机节点来运行它，这个过程成功与否、结果恰当与否，关键取决于容器编排系统是如何管理与分配集群节点的资源的。可以认为调度是必须以容器编排系统的资源管控为前提，那我们就先从Kubernetes的资源模型谈起。

### 14.1 资源模型

开篇先来厘清一个概念：资源是什么。资源在Kubernetes中是极为常用的术语，广义上讲，Kubernetes系统中所有能够接触的方方面面都被抽象成了资源，譬如表示工作负荷的资源（Pod、ReplicaSet、Service等），表示存储的资源（Volume、PersistentVolume、Secret等），表示策略的资源（SecurityContext、ResourceQuota、LimitRange等），表示身份的资源（ServiceAccount、Role、ClusterRole等）。“一切皆为资源”的设计是Kubernetes能够顺利施行声明式API的必要前提。Kubernetes以资源为载体，建立了一套同时囊括抽象元素（如策略、依赖、权限）和物理元素（如软件、硬件、网络）的领域特定语言。通过不同层级间资源的使用关系来描述上至整个集群甚至集群联邦，下至某一块内存区域或者一小部分处理器核心的状态，这些对资源状态的描述的集合，共同构成了一幅信息系统工作运行的全景图。

在11.2节里，笔者首次提到Kubernetes的资源模型，并将它与控制器模式一并列为Kubernetes中最重要的两个设计思想。本节，我们将再次讨论资源模型，但是这里所说的主要是狭义上的物理资源，特指排除了广义上那些逻辑方面的抽象资源，只包括能够与真实物理底层硬件对应的资源，譬如处理器资源、内存资源、磁盘存储资源，等等。由于我们讨论的话题是调度，作为调度最基本单位的Pod，只会与这些和物理硬件直接相关的资源产生供需关系，所以后文中提到资源，如无额外说明，均特指狭义上的物理资源。

从编排系统的角度来看，Node是资源的提供者，Pod是资源的使用者，调度是对两者进行恰当的撮合。Node通常能够提供三方面资源：计算资源（如处理器、图形处理器、内存）、存储资源（如磁盘容量、不同类型的介质）和网络资源（如带宽、网络地址）。其中与调度关系最密切的是处理器和内存，虽然它们同属于计算资源，但两者在调度时又有一些微妙的差别。处理器这样的资源被称作可压缩资源（Compressible Resource），特点是当可压缩资源不足时，Pod只会处于“饥饿状态”，运行变慢，但不会被系统杀死，即容器不会被直接终止，或被要求限时退出。而像内存这样的资源，则被称作不可压缩资源（Incompressible Resource），特点是当不可压缩资源不足，或者超过了容器自己声明的最大限度时，Pod就会因为内存溢出（Out-Of-Memory，OOM）而被系统直接杀掉。

Kubernetes给处理器资源设定的默认计量单位是“逻辑处理器的个数”。至于具体“一个逻辑处理器”应该如何理解，就要取决于节点的宿主机是如何解释的，通常会是/proc/cpuinfo中看到的处理器数量。它有可能是多路处理器系统上的一个处理器、多核处理器中的一个核心、云计算主机上的一个虚拟化处理器（Virtual CPU，vCPU），或者处理器核心里的一条超线程（Hyper-Threading）。总之，Kubernetes只负责保证Pod能够使用到“一个处理器”的计算能力，对不同硬件环境构成的Kubernetes集群，乃至同一个集群中不同硬件的宿主机节点来说，“一个处理器”所代表的真实算力完全有可能是不一样的。

在具体设置方面，Kubernetes沿用了云计算中处理器限额设置的一贯做法。如果不明确标注单位，譬如直接写0.5，默认单位就是Core，即0.5个处理器；也可以明确使用Millcore为单位，譬如写成500m同样代表0.5个处理器，因为Kubernetes规定了1 Core=1000 Millcores。而对于内存来说，它早已有广泛使用的计量单位，即Byte，如果设置中不明确标注单位就会默认以Byte计数。为了实际设置的方便，Kubernetes还支持Ei、Pi、Ti、Gi、Mi、Ki，以及E、P、T、G、M、K为单位，它们略微有一点点差别，以Mi和M为例，它们分别是Mebibyte与Megabyte的缩写，前者表示1024×1024 Bytes，后者表示1000×1000 Bytes。

### 14.2 服务质量与优先级

设定资源计量单位的目的是使管理员能够限制某个Pod对资源的过度占用，避免影响到其他Pod的正常运行。Pod由一到多个容器组成，资源最终交由Pod的各个容器去使用，所以资源的需求是设定在容器上的，具体的配置是Pod的spec.containers[].resource.limits/requests.cpu/memory字段。但是对资源需求的配额不是针对容器的，而是针对Pod整体，Pod的资源配额无须手动设置，它就是其包含的每个容器资源需求的累加值。

为容器设定最大的资源配额的做法从cgroups诞生后已经屡见不鲜，但你是否注意到Kubernetes给出的配置中有requests和limits两个设置项呢？这两者的区别其实很简单：requests是供调度器使用的，Kubernetes选择哪个节点运行Pod，只会根据requests的值来进行决策；limits才是供cgroups使用的，Kubernetes在向cgroups传递资源配额时，会按照limits的值来进行设置。

Kubernetes采用这样的设计完全是基于“心理学”的原因，因为Google根据Borg和Omega系统长期运行的实践经验总结出了一条经验法则：用户提交工作负载时设置的资源配额，并不是容器调度必须严格遵守的值，因为根据实际经验，大多数的工作负载在运行过程中真正使用到的资源，其实都远小于它所请求的资源配额。

![](../assets/c2575426d625b85b.jpg)额外知识

即使我们已经努力建议用户不要过度申请资源配额，但仍难免有大量用户过度消费，他们总希望避免因用户增长而产生资源不足的现象。

——“Large-Scale Cluster Management at Google with Borg”，Google

“多多益善”的想法完全符合人类的心理，大家提交的资源需求通常都是按照可能面临的最大压力去估计的，甚至考虑到了未来用户增长所导致的新需求。为了避免服务因资源不足而中断，都会往大了去申请，这点我们可以理解，但如果直接按照申请的资源去分配限额，所导致的结果必然是一方面服务器在大多数时间里都会有大量硬件资源闲置，另一方面这些闲置资源又已经分配出去，有了明确的所有者，不能再被其他人使用，难以真正发挥价值。

当然，仅依靠将一个资源配额的设置拆分成requests和limits两个设置项是不太可能解决这个矛盾的，Kubernetes为此还进行了许多额外的处理。一旦不按照最保守、最安全的方式去分配资源，就意味着容器编排系统必须为有可能出现的极端情况买单。如果允许节点给Pod分配的资源总和超过自己最大的可提供资源的话，假如某个时刻这些Pod的总消耗真的超标了，便会不可避免地导致节点无法继续遵守调度时对Pod许下的资源承诺，此时，Kubernetes只能杀掉一部分Pod腾出资源来保证其余Pod的正常运行，这个操作就是稍后会介绍的驱逐机制（Eviction）。要进行驱逐，首先Kubernetes就必须制定资源不足时该先牺牲哪些Pod、保留哪些Pod的明确准则，由此就形成了Kubernetes的服务质量等级（Quality of Service Level，QoS Level）和优先级（Priority）的概念。试想Kubernetes若不是为了理性对抗人类“多多益善”的心理，尽可能提高硬件利用效率，而是直接按申请的最大资源去安排调度，那原本它是无须理会这些麻烦事的。

质量等级是Pod的一个隐含属性，也是Kubernetes优先保障重要的服务，放弃一些没那么重要的服务的衡量标准。不知道你是否想到这样一个细节：如果不去设置limits和requests会怎样？如果不设置处理器和内存的资源，就意味着没有上限，该Pod可以使用节点上所有可用的计算资源。但你先别高兴得太早，虽然这类Pod能以最灵活的方式去使用资源，但也正是这类Pod扮演着最不稳定的风险来源的角色。在论文“Large-Scale Cluster Management at Google with Borg”[1]中，Google明确提出了针对这类Pod的一种近乎带惩罚性质的处理建议：当节点硬件资源不足时，优先杀掉这类Pod，说得文雅一点，就是给予这类Pod最低的服务质量等级。

Kubernetes目前提供的服务质量等级一共分为三级，由高到低分别为Guaranteed、Burstable和BestEffort。如果Pod中所有的容器都设置了limits和requests，且两者的值相等，那此Pod的服务质量等级便为最高的Guaranteed；如果Pod中有部分容器的requests值小于limits值，或者只设置了requests而未设置limits，那此Pod的服务质量等级为第二级Burstable；如果是上文说的那种情况，limits和requests两个都没设置则属于最低的BestEffort。

通常建议将数据库应用等有状态的应用，或者一些重要的必须不能中断的业务的服务质量等级定为Guaranteed，这样除非Pod使用超过了它们的limits所描述的不可压缩资源，或者节点的内存压力大到Kubernetes已经杀光所有等级更低的Pod了，否则它们都不会被系统自动杀死。相对地，应将一些临时的、不那么重要的任务设置为BestEffort，这样有利于调度时在更大的节点范围中寻找宿主机，也有利于在宿主机中利用更多的资源快速地完成任务，然后退出，尽量缩减影响范围；当然，遇到系统资源紧张时，它们也更容易被系统杀掉。

![](../assets/c2575426d625b85b.jpg)额外知识

所有动物生来平等，但有些动物比其他动物更加平等。

——《动物庄园》，乔治·奥威尔，1945年

除了服务质量等级以外，Kubernetes还允许系统管理员自行决定Pod的优先级，这是通过类型为PriorityClass的资源来实现的。优先级决定了Pod之间并不是平等的关系，且这种不平等不是谁会占用更多资源的问题，而是会直接影响Pod调度与生存的关键。

优先级会影响调度这很容易理解，它是指当多个Pod同时被调度的话，高优先级的Pod会优先被调度。Pod越晚被调度，就越大概率因节点资源已被占用而不能成功。但受优先级影响更大的另一方面是指Kubernetes的抢占机制（Preemption），在正常未设置优先级的情况下，如果Pod调度失败，就会暂时处于Pending状态被搁置起来，直到集群中有新节点加入或者旧Pod退出。但是，如果有一个被设置了明确优先级的Pod调度失败无法创建的话，Kubernetes就会在系统中寻找一批牺牲者（Victim），将它们杀掉以便给更高优先级的Pod让出资源。寻找的原则是根据在优先级低于待调度的Pod的所有已调度的Pod里，按照优先级从低到高排序，从最低的杀起，直至腾出的资源足以支持待调度Pod成功调度所需的资源为止，或者已经找不到更低优先级的Pod为止。

[1] 下载地址：https://pdos.csail.mit.edu/6.824/papers/borg.pdf。

### 14.3 驱逐机制

前面笔者动不动就说要杀掉某个Pod，听起来实在是欠优雅的，在Kubernetes中专业的称呼是“驱逐”（Eviction，即资源回收）。Pod的驱逐机制是通过kubelet来执行的，kubelet是部署在每个节点的集群管理程序，由于本身就运行在节点中，所以最容易感知到节点的资源实时消耗情况。kubelet一旦发现某种不可压缩资源将要耗尽时，就会主动终止节点上较低服务质量等级的Pod，以保证其他更重要的Pod的安全。被驱逐的Pod中的所有容器都会被终止，Pod的状态也会被更改为Failed。

我们已经接触过内存这一种最重要的不可压缩资源，默认配置下，前面所说的“资源即将耗尽”的“即将”，具体阈值是可用内存小于100Mi。除了可用内存（memory.available）外，其他不可压缩资源还包括宿主机的可用磁盘空间（nodefs.available）、文件系统可用inode数量（nodefs.inodesFree），以及可用的容器运行时镜像存储空间（imagefs.available）。后面三个的阈值都是按照实际容量的百分比来计算的，具体的默认值如下：

```
memory.available < 100Mi
nodefs.available < 10%
nodefs.inodesFree < 5%
imagefs.available < 15%
```

管理员可以在kubelet启动时，通过命令行参数来修改这些默认值，譬如可用内存只剩余100 Mi时才启动驱逐对于多数生产系统来说过于危险了，笔者建议在生产环境中考虑通过以下命令调整为剩余10%内存时开始驱逐：

```
$ kubelet --eviction-hard=memory.available<10%
```

如果你是一名Java、C#、Golang等习惯了自动内存管理机制的程序员，笔者还要提醒你的是Kubernetes的驱逐不能完全等同于编程语言中的垃圾收集。垃圾收集是安全的内存回收行为，而驱逐Pod是一种毁坏性的清理行为，有可能导致服务中断，必须更加谨慎。譬如，要同时兼顾硬件资源可能只是短时间内间歇性地超过了阈值的场景，以及资源正在被快速消耗，很快就会危及高服务质量的Pod甚至整个节点稳定性的场景。因此，驱逐机制中就有了软驱逐（Soft Eviction）、硬驱逐（Hard Eviction）以及优雅退出期（Grace Period）的概念。

·软驱逐：通常配置一个较低的警戒线（譬如可用内存仅剩20%），触及此线时，系统将进入一段观察期。如果只是暂时的资源抖动，在观察期内能够恢复到正常水平的话，那就不会真正启动驱逐操作。否则，若资源持续超过警戒线一段时间，就会触发Pod的优雅退出（Grace Shutdown），系统会通知Pod进行必要的清理工作（譬如将缓存的数据落盘），然后自行结束。在优雅退出期结束后，系统会强制杀掉还未曾自行了断的Pod。

·硬驱逐：通常配置一个较高的终止线（譬如可用内存仅剩10%），一旦触及此红线，立即强制杀掉Pod，而不会优雅退出。

软驱逐是为了减少资源抖动对服务的影响，硬驱逐是为了保障核心系统的稳定，它们并不矛盾，一般会同时使用，譬如以下例子所示：

```
$ kubelet --eviction-hard=memory.available<10% \
            --eviction-soft=memory.available<20% \
            --eviction-soft-grace-period=memory.available=1m30s \
            --eviction-max-pod-grace-period=600
```

Kubernetes的驱逐与编程语言中的垃圾收集的另一个不同之处是，垃圾收集可以“应收尽收”，而驱逐显然不行，不能无缘无故把整个节点中所有可驱逐的Pod都清空掉。但是，通常也不能只清理到刚刚低于警戒线就停止，必须考虑驱逐之后的新Pod调度与旧Pod运行的新增消耗。譬如kubelet驱逐了若干个Pod，让资源使用率勉强低于阈值，那么很可能在极短的时间内，资源使用率又会因某个Pod稍微占用了些许资源而重新超过阈值，再产生新的驱逐，如此往复。为此，Kubernetes提供了--eviction-minimum-reclaim参数设置一旦驱逐发生之后，至少清理出来多少资源才会终止。

不过，问题到这里还是没有全部解决，Kubernetes中很少会单独创建Pod，通常都是由ReplicaSet、Deployment等更高层资源来管理，这意味着当Pod被驱逐之后，它不会从此彻底消失，Kubernetes将自动生成一个新的Pod来取代，并经过调度选择一个节点继续运行。如果没有额外的处理，那很大概率这个Pod会被系统调度到当前节点上重新创建，因为上一次调度就选择了这个节点，而且这个节点刚刚驱逐完一批Pod得到了空闲资源，所以它显然符合此Pod的调度需求。为了避免上述情况，Kubernetes还提供了另一个参数--eviction-pressure-transition-period来约束调度器，设置在驱逐发生之后多长时间内不得往该节点调度Pod。

关于驱逐机制，你还应该意识到，这些措施既然被设计为以参数的形式开启，就说明了它们一定不是放之四海皆准的通用准则。举个例子，假设当前Pod是由DaemonSet控制的，一旦该Pod被驱逐，你又强行不允许节点在一段时间内接受调度，那显然这就有违DaemonSet的语义。目前Kubernetes并没有办法区分Pod是由DaemonSet抑或是别的高层次资源创建，因此这种假设情况确实有可能发生，比较合理的方案是让DaemonSet创建Guaranteed而不是BestEffort等级的Pod。总而言之，在Kubernetes还没有成熟到变为“傻瓜式”容器编排系统之前，因地制宜地配置和运维是非常必要的。

最后，服务质量、优先级、驱逐机制这些概念，都是在Pod层面上限制资源，是仅针对单个Pod的低层次约束，但现实中我们还常会遇到面向更高层次去控制资源的需求，譬如，想限制由多个Pod构成的微服务系统消耗的总资源，或者由多名成员组成的团队消耗的总资源。举个具体例子，想要在拥有32 GiB内存和16个处理器的集群里，允许A团队使用20 GiB内存和10个处理器的资源，再允许B团队使用10 GiB内存和4个处理器的资源，再预留2 GiB内存和2个处理器供将来分配。要满足这种资源限制的需求，Kubernetes的解决方案是先为它们建立一个专用的名称空间，然后在名称空间里建立ResourceQuota对象来描述如何进行整体的资源约束。

但是ResourceQuota与调度就没有直接关系了，它针对的对象也不是Pod，所以这里所说的资源可以是广义上的资源，不仅能够设置处理器、内存等物理资源的限额，还可以设置诸如Pod最大数量、ReplicaSet最大数量、Service最大数量、全部PersistentVolumeClaim的总存储容量等各种抽象资源的限额。甚至当Kubernetes预置的资源模型不能满足约束需要时，还能够根据实际情况去拓展，譬如要控制GPU的使用数量，完全可以通过Kubernetes的设备插件（Device Plugin）机制拓展出诸如nvidia.com/gpu:4这样的配置来。

### 14.4 默认调度器

本章的最后一节，我们回过头来探讨开篇提出的问题：Kubernetes是如何撮合Pod与Node的，这其实也是最难的一个问题。调度是为新创建出来的Pod寻找一个最恰当的宿主机节点去运行它，这句话里就包含“运行”和“恰当”两个调度中关键过程，具体分析如下。

·运行：从集群所有节点中找出一批剩余资源可以满足该Pod运行的节点。为此，Kubernetes调度器设计了一组名为Predicate的筛选算法。

·恰当：从符合运行要求的节点中找出一个最适合的节点完成调度。为此，Kubernetes调度器设计了一组名为Priority的评价算法。

这两个算法的具体内容稍后会详细解释，这里要先说明白一点：在几个、十几个节点的集群里进行调度，调度器怎么实现都不会太困难，但是对于数千个乃至更多节点的大规模集群，要实现高效的调度就绝不简单。请你想象一下，有一个由数千节点组成的集群，每次创建Pod都必须依据各节点的实时资源状态来确定调度的目标节点，然而各节点的资源是随着程序运行无时无刻不在变动的，资源状况只有节点本身最清楚，如果每次调度都要发生数千次的远程访问来获取这些信息的话，那压力与耗时都很难降下来，结果不仅会令调度器成为集群管理的性能瓶颈，还会出现因耗时过长，某些节点上资源状况已发生变化，调度器的资源信息过时而导致调度结果不准确等问题。

![](../assets/c2575426d625b85b.jpg)额外知识

由于调度器的工作负载与集群规模大致成正比，随着集群和它们的工作负载不断增长，调度器很有可能成为扩展性瓶颈所在。

——“Omega:Flexible,Scalable Schedulers for Large Compute Clusters”,Google

针对以上问题，Google在论文“Omega:Flexible,Scalable Schedulers for Large Compute Clusters”[1]里总结了自身的经验，并参考了当时Apache Mesos和Hadoop on Demand（HOD）的实现，提出了一种共享状态（Shared State）的双循环调度机制。这种调度机制后来不仅应用在Google的Omega系统（Borg的下一代集群管理系统）中，也同样被Kubernetes继承了下来，它的整体工作流程如图14-1所示。

![](../assets/c17b60a19b01486e.jpg)

图14-1　状态共享的双循环调度机制

“状态共享的双循环”中的第一个控制循环可被称为“Informer Loop”，它是一系列Informer[2]的集合，这些Informer持续监视etcd中与调度相关资源（主要是Pod和Node）的变化情况，一旦Pod、Node等资源出现变动，就会触发对应Informer的Handler。Informer Loop的职责是根据etcd中的资源变化去更新调度队列（Priority Queue）和调度缓存（Scheduler Cache）中的信息，譬如当有新Pod生成时，就将其入队（Enqueue）到调度队列中，如有必要，还会根据优先级触发上一节提到的插队和抢占操作。又譬如有新的节点加入集群，或者已有节点资源信息发生变动时，Informer也会将这些信息更新同步到调度缓存之中。

另一个控制循环可被称为“Scheduler Loop”，它的核心逻辑是不停地将调度队列中的Pod出队（Pop），然后使用Predicate算法进行节点选择。Predicate本质上是一组节点过滤器（Filter），它根据预设的过滤策略来筛选节点。Kubernetes中默认有三种过滤策略，分别如下所示。

·通用过滤策略：最基础的调度过滤策略，用来检查节点能否满足Pod声明中需要的资源需求。譬如处理器、内存资源是否满足，主机端口与声明的NodePort是否存在冲突，Pod的选择器或者nodeAffinity指定的节点是否与目标相匹配，等等。

·卷过滤策略：与存储相关的过滤策略，用来检查节点挂载的Volume是否存在冲突（譬如将一个块设备挂载到两个节点上），或者Volume的可用区域是否与目标节点冲突，等等。在13.1节中提到的Local PersistentVolume的调度检查，便是在这里处理的。

·节点过滤策略：与宿主机相关的过滤策略，最典型的是Kubernetes的污点与容忍度（Taint and Toleration）机制，譬如默认情况下Kubernetes会设置Master节点不允许被调度，这就是通过在Master中施加污点来避免的。之前提到的控制节点处于驱逐状态，或者在驱逐后一段时间不允许调度，也是在这个策略里实现的。

Predicate算法所使用的一切数据均来自于调度缓存，而绝对不会去远程访问节点本身。只有Informer Loop与etcd的监视操作才会涉及远程调用，Scheduler Loop中除了最后的异步绑定要发起一次远程的etcd写入外，其余都是进程内访问，这一点是调度器执行效率的重要保证。

调度缓存就是两个控制循环的共享状态（Shared State），这样的设计避免了每次调度时主动去轮询所有集群节点，保证了调度器的执行效率，但是并不能完全避免因节点信息同步不及时而导致调度过程中实际资源发生变化的情况，譬如节点的某个端口在获取调度信息后、发生实际调度前被意外占用了。为此，当调度结果出来之后，kubelet真正创建Pod之前，还必须执行一次Admit操作，在该节点上重新调用Predicate算法来进行二次确认。

经过Predicate算法筛选出符合要求的节点集，交给Priorities算法来打分（0～10分）并排序，以便挑选出“最恰当”的一个。“恰当”是带有主观色彩的词语，Kubernetes也提供了不同的打分规则来满足不同的主观需求，譬如最常用的LeastRequestedPriority规则，它的计算公式是：

```
score = (cpu((capacity-sum(requested))×10/capacity) + memory((capacity-
    sum(requested))×10/capacity))/2
```

从公式上很容易看出这就是在选择处理器和内存空闲资源最多的节点，因为这些资源剩余越多，得分就越高。经常与它配合使用的是BalancedResourceAllocation规则，它的公式是：

```
score = 10 - variance(cpuFraction,memoryFraction,volumeFraction)×10
```

此公式中cpuFraction、memoryFraction、volumeFraction的含义分别是Pod请求的处理器、内存和存储资源占该节点上对应可用资源的比例，variance函数的作用是计算资源之间的差距，差距越大，函数值越大。由此可知BalancedResourceAllocation规则的意图是希望调度完成后，所有节点里各种资源的分配尽量均衡，避免节点上出现诸如处理器资源被大量分配而内存大量剩余的尴尬状况。Kubernetes内置的评分规则还有ImageLocalityPriority、NodeAffinityPriority、TaintTolerationPriority等，有兴趣的读者可以阅读Kubernetes的源码，笔者就不再逐一解释了。

经过Predicate的筛选、Priorities的评分之后，调度器已经选出了调度的最终目标节点，最后一步是通知目标节点的kubelet去创建Pod。调度器并不会直接与kubelet通信来创建Pod，它只需要把待调度的Pod的nodeName字段更新为目标节点的名字即可，kubelet本身会监视该值的变化来接手后续工作。不过，从调度器在etcd中更新nodeName，kubelet从etcd中检测到变化，执行Admit操作二次确认调度可行性，最后到Pod开始实际创建的这个过程可能会持续一段不短的时间，如果一直等待这些工作都完成了才宣告调度最终完成，那势必也会显著影响调度器的效率。实际上Kubernetes调度器采用了乐观绑定（Optimistic Binding）的策略来解决此问题，它会同步更新调度缓存中Pod的nodeName字段，并异步更新etcd中Pod的nodeName字段，这个操作被称为绑定（Binding）。如果最终调度成功了，那etcd与调度缓存中的信息最终必定会保持一致，否则，如果调度失败了，那将会由Informer来根据Pod的变动，清空调度成功却没有创建成功的Pod的nodeName字段，重新同步回调度缓存中，以便促使另外一次调度的开始。

最后，请注意笔者在介绍这一节时用的标题是“默认调度器”，这是强调以上行为仅是Kubernetes默认的行为。对调度过程的大部分行为，你都可以通过Scheduler Framework暴露的接口来进行扩展和自定义，如图14-2所示，矩形箭头框的部分就是Scheduler Framework暴露的扩展点。由于Scheduler Framework属于Kubernetes内部的扩展机制（通过Golang的Plugin机制来实现，需静态编译），通用性与本章提到的其他扩展机制（CRI、CNI、CSI等）无法相提并论，属于较为高级的Kubernetes管理技能，所以这里笔者仅简单地提一下，就不多做介绍了。

![](../assets/fd97dbfb2beafb57.jpg)

图14-2　Scheduler Framework的可扩展性[3]

[1] 下载地址：https://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41684.pdf。

[2] Informer是Client-Go框架中的概念：https://godoc.org/k8s.io/client-go/informers。

[3] 图片来源：https://medium.com/dev-genius/kubernetes-scheduling-system-f8705e7ee226。
