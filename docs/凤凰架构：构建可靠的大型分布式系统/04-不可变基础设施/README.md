# 第四部分 不可变基础设施（§11–§15）

> 卡片结构：📖原文＝逐字引用（§N.M · uid NN 双锚点）｜🧭归纳＝编者从上述原文提炼，不冒充原文。来源：`00-原书档案/fulltext/uid-NN-*.md`

## §11 第11章 虚拟化容器

- **章节 UID**: 11
- **章节号**: §11
- **字数**: 37720
- **父模块**: 第四部分
- **原文出处**: [`uid-11-虚拟化容器.md`](../00-原书档案/fulltext/uid-11-虚拟化容器.md)

> 📖 **原文**（§11.1）：容器的起点可以追溯到1979年UNIX 7系统中提供的chroot命令，这个命令是英文单词“Change Root”的缩写，功能是当某个进程经过chroot操作之后，它的根目录就会被锁定在命令参数所指定的位置，以后它或者它的子进程将不能再访问和操作该目录之外的其他文件。

> 📖 **原文**（§11.1）：Linux的名称空间是一种由内核直接提供的全局资源封装，是内核针对进程设计的访问隔离机制。进程在一个独立的Linux名称空间中朝系统看去，会觉得自己仿佛就是这方天地的主人，拥有这台Linux主机上的一切资源，不仅文件系统是独立的，还有着独立的PID编号（譬如拥有自己的0号进程，即系统初始化的进程）、UID/GID编号（譬如拥有自己独立的root用户）、网络（譬如完全独立的IP地址、网络栈、防火墙等设置），等等，此时进程的心情简直不能再好了。

> 📖 **原文**（§11.1）：Linux系统解决以上问题的方案是控制群组（Control Groups，目前常用的简写为cgroups）。它与名称空间一样都是直接由内核提供功能，用于隔离或者分配并限制某个进程组能够使用的资源配额，资源配额包括处理器时间、内存大小、磁盘I/O速度等，具体可以参见表11-2。

> 📖 **原文**（§11.1）：LXC的出现肯定受到了OpenVZ和Linux-VServer的启发，站在巨人的肩膀上过河并没有什么不对。可惜的是，LXC在设定自己的发展目标时，也被前辈们的影响所局限住了。LXC眼中的容器与OpenVZ和Linux-VServer定义的并无差别，是一种封装系统的轻量级虚拟机，而Docker眼中的容器则是一种封装应用的技术手段。这两种封装理念在技术层面并没有什么本质区别，但应用效果差异巨大。

> 📖 **原文**（§11.1）：Kubernetes可谓出身名门，前身是Google内部已运行多年的集群管理系统Borg，于2014年6月使用Go语言完全重写后开源。自Kubernetes诞生之日起，只要与云计算稍微扯上关系的业界巨头都对Kubernetes争相追捧，IBM、Red Hat、Microsoft、VMware和华为都是它最早期的代码贡献者。

> 📖 **原文**（§11.2）：容器的本质是对cgroups和namespaces所提供的隔离能力的一种封装，在Docker提倡的单进程封装的理念影响下，容器蕴含的隔离性多了仅针对单个进程的额外限制，而Linux的cgroups和namespaces原本都是针对进程组而非单个进程来设计的，同一个进程组中的多个进程天然就可以共享相同的访问权限与资源配额。如果现在我们把容器与进程在概念上对应起来，那容器编排的第一个扩展点，就是要找到容器领域中与“进程组”相对应的概念，这是实现容器从隔离到协作的第一步，在Kubernetes的设计里，这个对应物叫作Pod。

> 📖 **原文**（§11.2）：所谓滚动更新（Rolling Update）是指先停止少量旧副本，维持大量旧副本继续提供服务，当停止的旧副本更新成功，新副本可以提供服务以后，再重复以上操作，直至所有的副本都更新成功。将这个过程放到ReplicaSet上，就是先创建新版本的ReplicaSet，然后一边让新的ReplicaSet逐步创建新版Pod的副本，一边让旧的ReplicaSet逐渐减少旧版Pod的副本。

> 📖 **原文**（§11.3）：Kustomize使用Base、Overlay和Patch生成最终配置文件的思路与Docker中分层镜像的思路有些相似，既规避了以“字符替换”对资源元数据文件的入侵，也不需要用户学习额外的DSL语法（譬如Lua）。

> 📖 **原文**（§11.3）：Operator将简洁的高级指令转化为Kubernetes中具体操作的方法，与前面Helm或者Kustomize的方法并不相同。Helm和Kustomize最终仍然是依靠Kubernetes的内置资源来跟Kubernetes打交道的，Operator则要求开发者自己实现一个专门针对该自定义资源的控制器，在控制器中维护自定义资源的期望状态。通过程序编码来扩展Kubernetes，比只通过内置资源来扩展要灵活得多，譬如当需要更新集群中某个Pod对象的时候，由Operator的开发者自己编码实现的控制器完全可以在原地对Pod进行重启，而无须像Deployment那样必须先删除旧的Pod，再创建新的Pod。

> 🧭 **归纳**：容器六步演进：①chroot（1979）=文件隔离起点，pivot_root（2000）补安全漏洞；②Namespace（2002 Mount→2006 增 UTS/IPC，现共 8 种）=访问隔离；③cgroups（2006 第一代→2016 第二代 v4.5）=资源配额；④LXC（2008）=封装系统的轻量虚拟机，受限 OpenVZ 思维定式；⑤Docker（2013）=封装应用 + 跨机器绿色部署 + 镜像生态，Dockerfile 单 ENTRYPOINT 强制单进程；⑥Kubernetes（2014，前身 Borg）=封装集群，靠 Google/CNCF 巨头加持必然胜出，Docker Swarm 已输编排战。容器→协作：cgroups/namespaces 原针对进程组，Pod 补足"容器组"概念，Pod 内默认共享 UTS/网络/IPC/时间 4 个 NS，仅 PID 与文件系统隔离，Infra Container（Pause Container）实现 NS 共享。韧性与弹性三件套：ReplicaSet 保故障自动恢复，Deployment 保滚动更新不中断，HPA 保水平扩缩容。应用封装谱系四代：①Kustomize=Base/Overlay/Patch YAML 模板；②Helm=Chart+Repository+Release，模拟 apt/yum 但无状态服务管理；③Operator=CRD+自定义控制器，程序化扩展 K8s 解决有状态运维；④OAM（阿里+微软 2019）=Component+Workload+Trait+Scope+Application Configuration 分离开发/运维/平台三角色关注点。Operator CRD 实例：Elasticsearch CR 把"部署 3 节点 7.9.1 ES"压到 10 行 YAML。

## §12 第12章 容器间网络

- **章节 UID**: 12
- **章节号**: §12
- **字数**: 27169
- **父模块**: 第四部分
- **原文出处**: [`uid-12-容器间网络.md`](../00-原书档案/fulltext/uid-12-容器间网络.md)

> 📖 **原文**（§12.1）：在图12-1中传输模型的左侧，笔者特别标出了网络栈在用户空间与内核空间的部分，可见几乎整个网络栈（应用层以下）都位于系统内核空间之中。之所以采用这种设计，主要是从数据安全隔离的角度来考虑的。由内核去处理网络报文的收发，无疑会有更高的执行开销，譬如数据在内核态和用户态之间来回复制的额外成本，因此会损失一些性能，但是能够保证应用程序无法窃听或者伪造另一个应用程序的通信内容。

> 📖 **原文**（§12.1）：网络协议栈的处理是一套相对固定和封闭的流程，整套处理过程中，除了在网络设备层能看到一点点程序以设备的形式介入处理的空间外，其他过程似乎就没有什么可供程序插手的空间了。然而事实并非如此，从Linux Kernel 2.4版本开始，内核开放了一套通用的、可供代码干预数据在协议栈中流转的过滤器框架。这套名为Netfilter的框架是Linux防火墙和网络的主要维护者Rusty Russell提出并主导设计的，它围绕网络层（IP协议）的周围，埋下了五个钩子（Hook），每当有数据包流到网络层，经过这些钩子时，就会自动触发由内核模块注册在这里的回调函数，这样程序代码就能够通过回调函数来干预Linux的网络通信，如图12-2所示。

> 📖 **原文**（§12.1）：veth是另外一种主流的虚拟网卡方案，在Linux Kernel 2.6版本，Linux在开始支持网络名称空间隔离的同时，也提供了专门的虚拟以太网（Virtual Ethernet，习惯简写做veth）让两个隔离的网络名称空间之间可以互相通信。直接把veth比喻成虚拟网卡其实并不准确，如果要和物理设备类比，它应该相当于由交叉网线连接的一对物理网卡。

> 📖 **原文**（§12.1）：Linux Bridge是在Linux Kernel 2.2版本开始提供的二层转发工具，由brctl命令创建和管理。Linux Bridge创建以后，便能够接入任何位于二层的网络设备，无论是真实的物理设备（譬如eth0）抑或是虚拟设备（譬如veth或者tap）都能与Linux Bridge配合工作。当有二层数据包（以太帧）从网卡进入时Linux Bridge将根据数据包的类型和目标MAC地址，按如下规则转发处理。

> 📖 **原文**（§12.1）：VXLAN对网络基础设施的要求很低，不需要专门的硬件提供的特别支持，只要三层可达的网络就能部署VXLAN。VXLAN的每个边缘入口上都布置了一个VTEP（VXLAN Tunnel Endpoint）设备，它既可以是物理设备，也可以是虚拟化设备，负责VXLAN协议报文的封包和解包。互联网号码分配局（Internet Assigned Numbers Authority，IANA）专门分配了4789作为VTEP设备的UDP端口（以前Linux VXLAN用的默认端口是8472，目前这两个端口在许多场景中仍有并存的情况）。

> 📖 **原文**（§12.1）：·桥接模式，使用--network=bridge指定，这也是未指定网络参数时的默认网络。桥接模式下，Docker会为新容器分配独立的网络名称空间，创建好veth pair，一端接入容器，另一端接入docker0网桥。Docker会为每个容器自动分配好IP地址，默认配置下地址范围是172.17.0.0/24，docker0的地址默认是172.17.0.1，并且设置所有容器的网关为docker0，这样所有接入同一个网桥内的容器可以直接依靠二层网络来通信，而在此范围之外的容器、主机就必须通过网关来访问，具体过程笔者在介绍Linux Bridge时已经详细讲解过，这里不再赘述。

> 📖 **原文**（§12.2）：如今CNM与容器网络的事实标准CNI（Container Networking Interface，容器网络接口）在目标上几乎是完全重叠的，由此决定了CNM与CNI之间只能是“你死我活”的竞争关系，这与容器运行时中提及的CRI和OCI的关系明显不同，CRI与OCI的目标并不一样，两者有足够的空间可以和平共处。

> 📖 **原文**（§12.2）：由测试结果可见，MACVLAN和SR-IOV这样的Underlay网络插件的吞吐量最高、延迟最低，仅从网络性能上看它们肯定是最优秀的，而Flannel-VXLAN这样的Overlay网络插件，其吞吐量只有MACVLAN和SR-IOV的70%左右，延迟却高了两至三倍之多。可见Overlay为了易用性、灵活性所付出的代价还是不可忽视的，但是对于那些不以网络I/O为性能瓶颈的系统而言，这样的代价并非一定不可接受，就看你如何对通用性与性能进行权衡取舍。

> 🧭 **归纳**：网络栈四层封装：Socket→TCP/UDP→IP→Device→Driver，全程在内核态保证安全。Netfilter 五钩子：PREROUTING（DNAT）/INPUT/FORWARD/OUTPUT/POSTROUTING（SNAT），iptables 在此基础上叠 5 张表（raw→mangle→nat→filter→security），kube-proxy 靠 iptables/IPVS 做 ClusterIP→Pod NAT。虚拟网络设备四件套：①tun/tap（Kernel 2.4，模拟二/三层网卡，做隧道/字符设备）；②veth pair（Kernel 2.6，"交叉网线"对端，性能优，几行代码即可实现）；③Linux Bridge（Kernel 2.2，二层交换+MAC 学习+STP）；④VXLAN（Kernel 3.7 完整支持，IANA 端口 4789，24 位 VNI = 1677 万，UDP/IP/以太帧额外 50 字节头，Macvlan 是 VLAN 子接口思想延伸）。Docker 三网络：bridge（默认 docker0，172.17.0.0/24）/host（共享宿主 NS，端口冲突）/none（仅回环）；另支持 container/MACVLAN/Overlay 模式。容器网络标准战：CNM（Docker 2015.05 libnetwork）vs CNI（K8s+CoreOS 2015.07 rkt 提案）→五年后 CNI 完胜（K8s/RKT/ECS/OpenShift/Mesos/Cloud Foundry 全部加入，Contiv/Calico/Weave 转投 CNI）。CNI 插件三类：①Overlay（Flannel-VXLAN/Calico-IPIP/Weave）通用但性能-30%；②Routing（Flannel-HostGW/Calico-BGP）性能接近裸金属，依赖二层连通或 BGP；③Underlay（MACVLAN/SR-IOV）吞吐最高延迟最低，但硬件依赖强。

## §13 第13章 持久化存储

- **章节 UID**: 13
- **章节号**: §13
- **字数**: 24000
- **父模块**: 第四部分
- **原文出处**: [`uid-13-持久化存储.md`](../00-原书档案/fulltext/uid-13-持久化存储.md)

> 📖 **原文**（§13.1）：Mount和Volume都是源自操作系统的常用术语。Mount是动词，表示将某个外部存储挂载到系统中；Volume是名词，表示物理存储的逻辑抽象，目的是为物理存储提供有弹性的分割方式。容器源于对操作系统层的虚拟化，为了满足容器内生成数据的外部存储需求，很自然地会将Mount和Volume的概念延拓至容器中。

> 📖 **原文**（§13.1）：目前，Docker内置了三种挂载类型，分别是Bind（--mount type=bind）、Volume（--mount type=volume）和tmpfs（--mount type=tmpfs），如图13-1所示。其中tmpfs用于在内存中读写临时数据，不属于本节主要讨论的对象持久化存储范畴，所以后面我们只着重关注Bind和Volume两种挂载类型。

> 📖 **原文**（§13.1）：Kubernetes对PersistentVolumeClaim与PersistentVolume的撮合结果是产生一对一的绑定关系，“一对一”的意思是PersistentVolume一旦绑定在某个PersistentVolumeClaim上，直到释放以前都会被这个PersistentVolumeClaim所独占，不能再与其他Persistent-VolumeClaim进行绑定。这意味着即使PersistentVolumeClaim申请的存储空间比Persistent-Volume能够提供的要少，依然要求整个存储空间都为该PersistentVolumeClaim所用，这有可能会造成资源的浪费。

> 📖 **原文**（§13.1）：Dynamic Provisioning与Static Provisioning并不是各有用途的互补设计，而是对同一个问题先后出现的两种解决方案。你完全可以只用Dynamic Provisioning来满足所有Static Provisioning能够满足的存储需求，包括那些不需要动态分配的场景，甚至之前例子里使用HostPath在本地静态分配存储的操作，都可以指定no-provisioner作为资源分配器的StorageClass，以Local Persistent Volume来代替，譬如以下例子所示：

> 📖 **原文**（§13.2）：以上提到的Provision、Delete、Attach、Detach、Mount、Unmount六种操作，并不是直接由Kubernetes来实现，而是在存储插件中完成的，它们会分别被Kubernetes通过两个控制器及一个管理器来调用，如图13-6所示，这些控制器、管理器的作用分别如下。

> 📖 **原文**（§13.2）：相比FlexVolume的种种不足，CSI可以说是一个十分完善的存储扩展规范，这里的“十分完善”并不是客套话，根据GitHub的自动代码行统计，FlexVolume的规范文档仅有155行，而CSI则长达2704行。

> 📖 **原文**（§13.2）：因此，当Kubernetes成为市场主流以后——准确地说是从1.14版本开始，Kubernetes启动了In-Tree存储驱动的CSI外置迁移工作。按照计划，在1.21到1.22版本（大约在2021年中期）时，Kubernetes中主要的存储驱动，如AWS EBS、GCE PD、vSphere等都会迁移至符合CSI规范的Out-of-Tree实现，不再提供对In-Tree的支持。

> 📖 **原文**（§13.2）：得益于NFS的天然特性，EFS的扩缩可以是完全自动、实时的，创建新文件时无须预置存储，删除已有文件时也不必手动缩容以节省费用。在高性能网络的支持下，EFS的性能已经能够达到相当高的水平，尽管由于网络访问的限制，性能最高的EFS依然比不过最高水平的EBS，但仍然能充分满足绝大多数应用运行的需要。还有最重要的一点优势是由于脱离了块设备的束缚，EFS能够轻易地被成百上千个EC2实例共享，考虑到EFS的性能、动态弹性、可共享等因素，笔者给出的明确建议是它可以作为大部分容器工作负载的首选存储。

> 🧭 **归纳**：镜像稳定 vs 数据持久的矛盾由容器 Copy-on-Write（OverlayFS 叠加）解决，默认不持久。Docker 三种 Mount：Bind（最早，跨主机靠预挂 NFS，Docker 无法管理）、Volume（Docker 17.06 起 --mount type=volume，可对接 Volume Driver/Storage Driver）、tmpfs（内存）。Kubernetes Volume 演化：①普通 Volume=Pod 内部容器共享，生命周期跟 Pod；②PersistentVolume（PV）=管理员预置网络存储，独立于 Pod；③PersistentVolumeClaim（PVC）=用户声明存储需求，PV/PVC 一对一绑定（易浪费，3GB 申请要独占 5GB PV）；④StorageClass + Dynamic Provisioning（v1.6+）=Provisioner 按需自动分配，回收策略废弃 Recycle（粗暴 rm -rf），Retain/Delete 仍保留；⑤Local PV（v1.10）=本地磁盘，Volume Binding 模式必考虑节点分布。三种存储类型：①块存储（EBS/iSCSI/SCSI）=贴近硬件，吞吐量高延迟低，但 RWO 排他；②文件存储（EFS/NFS，POSIX 接口）=树状目录 + 权限，自动扩缩，可被成百 EC2 共享，容器首选；③对象存储（S3）=REST Endpoint+扁平 Bucket，元数据+数据块，吞吐高延迟差，便宜一两个数量级，适合 CDN/备份/归档。Kubernetes 存储架构三步走：Provision→Attach→Mount（PV Controller / AD Controller / Volume Manager），对应 Delete/Detach/Unmount 逆操作。FlexVolume（v1.2→v1.8 GA）vs CSI（v1.9→v1.13 GA，2704 行 vs 155 行规范）：CSI 三 gRPC 接口（Identity/Controller/Node），以 StatefulSet+DaemonSet 部署，CSIMigration（v1.17）保证 In-Tree 平滑迁 Out-of-Tree。

## §14 第14章 资源与调度

- **章节 UID**: 14
- **章节号**: §14
- **字数**: 12040
- **父模块**: 第四部分
- **原文出处**: [`uid-14-资源与调度.md`](../00-原书档案/fulltext/uid-14-资源与调度.md)

> 📖 **原文**（§14.1）：其中与调度关系最密切的是处理器和内存，虽然它们同属于计算资源，但两者在调度时又有一些微妙的差别。处理器这样的资源被称作可压缩资源（Compressible Resource），特点是当可压缩资源不足时，Pod只会处于“饥饿状态”，运行变慢，但不会被系统杀死，即容器不会被直接终止，或被要求限时退出。而像内存这样的资源，则被称作不可压缩资源（Incompressible Resource），特点是当不可压缩资源不足，或者超过了容器自己声明的最大限度时，Pod就会因为内存溢出（Out-Of-Memory，OOM）而被系统直接杀掉。

> 📖 **原文**（§14.2）：为容器设定最大的资源配额的做法从cgroups诞生后已经屡见不鲜，但你是否注意到Kubernetes给出的配置中有requests和limits两个设置项呢？这两者的区别其实很简单：requests是供调度器使用的，Kubernetes选择哪个节点运行Pod，只会根据requests的值来进行决策；limits才是供cgroups使用的，Kubernetes在向cgroups传递资源配额时，会按照limits的值来进行设置。

> 📖 **原文**（§14.2）：Kubernetes目前提供的服务质量等级一共分为三级，由高到低分别为Guaranteed、Burstable和BestEffort。如果Pod中所有的容器都设置了limits和requests，且两者的值相等，那此Pod的服务质量等级便为最高的Guaranteed；如果Pod中有部分容器的requests值小于limits值，或者只设置了requests而未设置limits，那此Pod的服务质量等级为第二级Burstable；如果是上文说的那种情况，limits和requests两个都没设置则属于最低的BestEffort。

> 📖 **原文**（§14.2）：优先级会影响调度这很容易理解，它是指当多个Pod同时被调度的话，高优先级的Pod会优先被调度。Pod越晚被调度，就越大概率因节点资源已被占用而不能成功。但受优先级影响更大的另一方面是指Kubernetes的抢占机制（Preemption），在正常未设置优先级的情况下，如果Pod调度失败，就会暂时处于Pending状态被搁置起来，直到集群中有新节点加入或者旧Pod退出。但是，如果有一个被设置了明确优先级的Pod调度失败无法创建的话，Kubernetes就会在系统中寻找一批牺牲者（Victim），将它们杀掉以便给更高优先级的Pod让出资源。

> 📖 **原文**（§14.3）：前面笔者动不动就说要杀掉某个Pod，听起来实在是欠优雅的，在Kubernetes中专业的称呼是“驱逐”（Eviction，即资源回收）。Pod的驱逐机制是通过kubelet来执行的，kubelet是部署在每个节点的集群管理程序，由于本身就运行在节点中，所以最容易感知到节点的资源实时消耗情况。kubelet一旦发现某种不可压缩资源将要耗尽时，就会主动终止节点上较低服务质量等级的Pod，以保证其他更重要的Pod的安全。被驱逐的Pod中的所有容器都会被终止，Pod的状态也会被更改为Failed。

> 📖 **原文**（§14.3）：·软驱逐：通常配置一个较低的警戒线（譬如可用内存仅剩20%），触及此线时，系统将进入一段观察期。如果只是暂时的资源抖动，在观察期内能够恢复到正常水平的话，那就不会真正启动驱逐操作。否则，若资源持续超过警戒线一段时间，就会触发Pod的优雅退出（Grace Shutdown），系统会通知Pod进行必要的清理工作（譬如将缓存的数据落盘），然后自行结束。在优雅退出期结束后，系统会强制杀掉还未曾自行了断的Pod。

> 📖 **原文**（§14.4）：Predicate算法所使用的一切数据均来自于调度缓存，而绝对不会去远程访问节点本身。只有Informer Loop与etcd的监视操作才会涉及远程调用，Scheduler Loop中除了最后的异步绑定要发起一次远程的etcd写入外，其余都是进程内访问，这一点是调度器执行效率的重要保证。

> 🧭 **归纳**：调度前提=资源管控，"一切皆资源"是声明式 API 前提。物理资源两类：①可压缩（CPU，1 Core=1000m，500m=0.5 核）=饥饿不死；②不可压缩（Memory+OOM）=直接杀容器。requests vs limits 双轨制（来自 Borg/Omega 经验）：用户倾向"多多益善"过度申请→拆出 requests 给调度、limits 给 cgroups→资源分配有余裕→必须设计驱逐。QoS 三档：①Guaranteed（所有容器 limits=requests）=等级最高；②Burstable（requests<limits 或单设）=中间；③BestEffort（都不设）=节点资源不足最先杀，灵活但最不稳定。Priority+Preemption：高优先级 Pod 调度失败→找一批 Victim（按低到高优先级排）杀掉让位。驱逐机制：默认阈值 memory.available<100Mi / nodefs.available<10% / nodefs.inodesFree<5% / imagefs.available<15%，生产建议 10%；软驱逐（低警戒线 + 观察期 + 优雅退出）vs 硬驱逐（高红线 + 立即杀），配合 --eviction-minimum-reclaim 防反复抖动 + --eviction-pressure-transition-period 防刚驱逐完又调度回来。Namespace 级 ResourceQuota 控总量，Device Plugin（如 nvidia.com/gpu:4）扩展自定义硬件资源。默认调度器双循环：①Informer Loop 监视 etcd 更新 Priority Queue + Scheduler Cache；②Scheduler Loop 出队 Pod→Predicate（Filter）三策略：通用（CPU/内存/NodePort/NodeAffinity）/卷（PV 冲突 + Local PV 区域）/节点（Taint-Toleration + 驱逐状态）；→Priorities 打分（0~10），LeastRequestedPriority（最空闲）+ BalancedResourceAllocation（最均衡）；→Optimistic Binding 异步更新 etcd；→kubelet Admit 二次确认。Scheduler Framework 暴露扩展点（Golang Plugin，静态编译）。

## §15 第15章 服务网格

- **章节 UID**: 15
- **章节号**: §15
- **字数**: 21833
- **父模块**: 第四部分
- **原文出处**: [`uid-15-服务网格.md`](../00-原书档案/fulltext/uid-15-服务网格.md)

> 📖 **原文**（§15.1）：如果说边车代理还有什么不足之处的话，那大概就是来自于运维人员的不满了。边车代理能够透明且具有强制力地解决可靠通信的问题，但它本身也需要有足够的信息才能完成这项工作，譬如获取可用服务的列表，譬如得到每个服务名称对应的IP地址，等等。这些信息不会自动到边车里去，需要由管理员主动去告知代理，或者代理主动从约定的好的位置获取。可见，管理代理本身也会产生额外的通信需求。如果没有额外的支持，这些管理方面的通信都得由运维人员去埋单，由此而生的不满便可以理解。为了管理与协调边车代理，程序间通信进化到了最后一个阶段：服务网格。

> 📖 **原文**（§15.1）：用iptables进行流量劫持是最经典、最通用的手段，不过，iptables重定向流量必须通过回环设备交换数据，即流量不得不多穿越一次协议栈，如图15-6所示。

> 📖 **原文**（§15.1）：Envoy在这方面进行了创新，它将代理转发的行为规则抽象成Listener、Router、Cluster三种资源，以此为基础，又定义了应该如何发现和访问这些资源的一系列API，现在这些资源和API被统称为“xDS协议族”，如图15-8所示。自此以后，数据平面就有了如何描述各种配置和策略的事实标准，控制平面也有了与控制平面交互的标准接口。

> 📖 **原文**（§15.1）：·Listener：Listener可以简单理解为Envoy的一个监听端口，用于接收来自下游应用程序（Downstream）的数据。Envoy能够同时支持多个Listener，不同的Listener之间的策略配置是相互隔离的。

> 📖 **原文**（§15.1）：从1.5版本起，Istio重新回归单体架构，将Pilot、Galley、Citadel的功能全部集成到新的istiod之中，如图15-9所示。当然，这也并不是说完全推翻之前的设计，只是将原有的多进程形态优化成单进程的形态，之前各个独立组件变成了istiod的内部逻辑上的子模块而已。

> 📖 **原文**（§15.2）：在2019年5月的KubeCon大会上，微软联合Linkerd、HashiCorp、Solo、Kinvolk和Weaveworks等一批云原生服务商共同宣布了Service Mesh Interface规范，希望能在各家的服务网格产品之上建立一个抽象的API层，然后通过这个抽象层来解耦和屏蔽底层服务网格实现，让上层的应用、工具、生态系统可以建立在同一个业界标准之上，从而实现应用程序在不同服务网格产品之间的无缝移植与互通。

> 📖 **原文**（§15.2）：Istio：Google、IBM和Lyft公司联手打造的产品，以自己的Envoy为默认数据平面。Istio是目前功能最强大的服务网格，如果你苦恼于这方面产品的选型，直接挑选Istio不一定是最合适的，但起码能保证这是不会有明显缺陷的选择；同时Istio也是市场占有率第一的控制平面，不少公司发布的服务网格产品都是在它的基础上派生增强而来，譬如蚂蚁金服的SOFAMesh、Google Cloud Service Mesh等。

> 🧭 **归纳**：服务网格=William Morgan 2017 定义，处理程序间通信基础设施，边车代理+控制器。通信五阶段演进：①业务代码耦合（OKHTTP/gRPC 库内嵌容错逻辑）；②公共组件库解耦（Twitter Finagle / Spring Cloud，但绑语言）；③独立网络代理（Netfilix Prana 模式）；④边车代理+iptables 强制流量劫持（Linkerd/Envoy/MOSN，透明）；⑤数据/控制平面分离（服务网格成熟形态）。数据平面三关键：①代理注入=基座模式（ServiceComb Mesher，侵入）/手动注入（改 Pod YAML）/自动注入（Istio 用 MutatingWebhookConfiguration 匹配 istio-injection=enabled 标签，Webhook 调 istio-sidecar-injector /inject）；②流量劫持=iptables REDIRECT（15001 出/15006 入，init 容器 istio-iptables 写入 PREROUTING+OUTPUT 链），iptables 经回环多穿协议栈，性能损耗→eBPF Socket 层直转是前沿；③可靠通信=Envoy xDS 三资源（Listener 监下游/LDS、Cluster 上下游服务池/CDS+EDS、Router 网关转发/RDS）+ Filter 插件机制。控制平面：Istio 1.5 前微服务架构（Mixer 鉴权遥测 / Pilot xDS 分发 / Galley 配置 / Citadel CA）被批过度设计→1.5 起单体 istiod 集成全部，职责含边车注入、策略/配置分发（CRD/MCP）、流量控制（VirtualService+DestinationRule，金丝雀/熔断/重试/负载均衡/故障注入/流量镜像）、通信安全（SDS 替代 Secret 卷，证书内存传递不重启）、可观测（日志/Tracing/Metrics）。规范两件套：①SMI（微软 2019.05 KubeCon，2020.04 入 CNCF Sandbox）=Kubernetes Native + Provider Agnostic，对标 Istio VirtualService/DestinationRule/Gateway，含 Traffic Specs/Split/Metric/Access Control 四 API（均 Alpha）；②UDPA（UDPA-WG 2019.05，对标 SDN OpenFlow）=Envoy xDS v4 雏形，分 UDPA-TP 传输+UDPA-DM 数据模型，Alpha→Stable→Deprecated→Removed 各一年周期。生态数据面：Linkerd（CNCF 2017-01 孵化，Scala/JVM 已失势）vs Envoy（CNCF 2017-09，C++，xDS 公开，市场第一）vs nginMesh（2020 No Longer Active）vs Linkerd 2（Rust 重写，性能赶 Envoy）vs MOSN（Golang，2018-06 蚂蚁金服开源，2019-12 入 CNCF）；控制面：Istio（功能最强大，Google/IBM/Lyft 主导）vs Linkerd 2（创业公司挑战者）vs Consul Connect（HashiCorp 集成定位）。
